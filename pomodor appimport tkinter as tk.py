import base64
import json
import os
import secrets
import string
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

try:
	from cryptography.fernet import Fernet, InvalidToken
	from cryptography.hazmat.primitives import hashes
	from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
	Fernet = InvalidToken = hashes = PBKDF2HMAC = None


VAULT_PATH = os.path.join(os.path.expanduser("~"), ".tk_password_manager.json")
ITERATIONS = 390_000


def derive_key(password, salt):
	kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITERATIONS)
	return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))


class PasswordManager:
	def __init__(self, root):
		self.root = root
		self.root.title("Password Manager")
		self.root.geometry("620x460")
		self.root.minsize(520, 380)
		self.entries = []
		self.fernet = None

		if Fernet is None:
			messagebox.showerror("Dependency required", "Install cryptography first:\n\npip install cryptography", parent=root)
			root.destroy()
			return
		self.build_ui()
		self.unlock()

	def build_ui(self):
		main = ttk.Frame(self.root, padding=14)
		main.pack(fill="both", expand=True)
		form = ttk.LabelFrame(main, text="Add account", padding=10)
		form.pack(fill="x")
		form.columnconfigure(1, weight=1)

		self.site = tk.StringVar()
		self.username = tk.StringVar()
		self.password = tk.StringVar()
		for row, (label, variable) in enumerate((("Website / service", self.site), ("Username", self.username), ("Password", self.password))):
			ttk.Label(form, text=label + ":").grid(row=row, column=0, sticky="w", padx=(0, 10), pady=4)
			ttk.Entry(form, textvariable=variable, show="•" if row == 2 else "").grid(row=row, column=1, sticky="ew", pady=4)
		ttk.Button(form, text="Generate", command=self.generate).grid(row=2, column=2, padx=(8, 0))
		ttk.Button(form, text="Save account", command=self.save).grid(row=3, column=1, sticky="e", pady=(8, 0))

		listing = ttk.LabelFrame(main, text="Saved accounts", padding=8)
		listing.pack(fill="both", expand=True, pady=12)
		listing.columnconfigure(0, weight=1)
		listing.rowconfigure(0, weight=1)
		self.tree = ttk.Treeview(listing, columns=("site", "username"), show="headings", selectmode="browse")
		self.tree.heading("site", text="Website / service")
		self.tree.heading("username", text="Username")
		self.tree.grid(row=0, column=0, sticky="nsew")
		scrollbar = ttk.Scrollbar(listing, orient="vertical", command=self.tree.yview)
		scrollbar.grid(row=0, column=1, sticky="ns")
		self.tree.configure(yscrollcommand=scrollbar.set)
		buttons = ttk.Frame(main)
		buttons.pack(fill="x")
		ttk.Button(buttons, text="Copy selected password", command=self.copy_selected).pack(side="left")
		ttk.Button(buttons, text="Delete selected", command=self.delete_selected).pack(side="left", padx=8)
		ttk.Label(buttons, text="Encrypted local vault").pack(side="right")

	def unlock(self):
		new_vault = not os.path.exists(VAULT_PATH)
		prompt = "Create a master password for your new vault:" if new_vault else "Enter your master password:"
		password = simpledialog.askstring("Unlock vault", prompt, show="•", parent=self.root)
		if password is None:
			self.root.destroy()
			return
		if not password:
			messagebox.showerror("Invalid password", "Master password cannot be empty.", parent=self.root)
			self.root.destroy()
			return
		try:
			if new_vault:
				self.salt = os.urandom(16)
				self.fernet = Fernet(derive_key(password, self.salt))
				self.write_vault()
			else:
				with open(VAULT_PATH, encoding="utf-8") as file:
					stored = json.load(file)
				if stored.get("version") != 1:
					raise ValueError("Unsupported vault version")
				self.salt = base64.b64decode(stored["salt"])
				self.fernet = Fernet(derive_key(password, self.salt))
				decrypted = self.fernet.decrypt(stored["data"].encode("ascii"))
				self.entries = json.loads(decrypted.decode("utf-8"))
				if not isinstance(self.entries, list):
					raise ValueError("Invalid vault data")
			self.refresh()
		except (InvalidToken, KeyError, ValueError, OSError, json.JSONDecodeError):
			messagebox.showerror("Vault error", "Unable to open the vault. Check the master password or vault file.", parent=self.root)
			self.root.destroy()

	def write_vault(self):
		encrypted = self.fernet.encrypt(json.dumps(self.entries).encode("utf-8")).decode("ascii")
		data = {"version": 1, "salt": base64.b64encode(self.salt).decode("ascii"), "data": encrypted}
		temporary = VAULT_PATH + ".tmp"
		with open(temporary, "w", encoding="utf-8") as file:
			json.dump(data, file)
		os.replace(temporary, VAULT_PATH)

	def refresh(self):
		self.tree.delete(*self.tree.get_children())
		for index, item in enumerate(self.entries):
			self.tree.insert("", "end", iid=str(index), values=(item["site"], item["username"]))

	def generate(self):
		alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}?"
		self.password.set("".join(secrets.choice(alphabet) for _ in range(20)))

	def save(self):
		site, username, password = self.site.get().strip(), self.username.get().strip(), self.password.get()
		if not site or not username or not password:
			messagebox.showwarning("Missing details", "Enter a website, username, and password.", parent=self.root)
			return
		self.entries.append({"site": site, "username": username, "password": password})
		try:
			self.write_vault()
		except OSError as error:
			self.entries.pop()
			messagebox.showerror("Save error", str(error), parent=self.root)
			return
		self.refresh()
		self.site.set("")
		self.username.set("")
		self.password.set("")

	def copy_selected(self):
		selection = self.tree.selection()
		if not selection:
			messagebox.showinfo("Select account", "Choose an account first.", parent=self.root)
			return
		self.root.clipboard_clear()
		self.root.clipboard_append(self.entries[int(selection[0])]["password"])
		self.root.update()
		messagebox.showinfo("Copied", "Password copied to clipboard.", parent=self.root)

	def delete_selected(self):
		selection = self.tree.selection()
		if not selection:
			messagebox.showinfo("Select account", "Choose an account first.", parent=self.root)
			return
		if not messagebox.askyesno("Delete account", "Permanently delete this account?", parent=self.root):
			return
		index = int(selection[0])
		removed = self.entries.pop(index)
		try:
			self.write_vault()
		except OSError as error:
			self.entries.insert(index, removed)
			messagebox.showerror("Save error", str(error), parent=self.root)
			return
		self.refresh()


if __name__ == "__main__":
	app = tk.Tk()
	PasswordManager(app)
	app.mainloop()
