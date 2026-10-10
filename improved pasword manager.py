import tkinter as tk
from tkinter import messagebox
import random
import json


# ---------------------------- INDEPENDENT LOGIC FUNCTION ------------------------------- #
def create_secure_string(length=12):
    """
    یہ ایک بالکل الگ اور خود مختار فنکشن ہے جو آپ کی ضرورت کے مطابق
    ایک مضبوط پاس ورڈ تیار کر کے واپس (Return) کرتا ہے۔
    """
    letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '0123456789'
    symbols = '!#$%&()*+'

    # پاس ورڈ میں ہر قسم کے کیریکٹرز کا ہونا لازمی بنانا
    pass_letters = [random.choice(letters) for _ in range(length - 4)]
    pass_symbols = [random.choice(symbols) for _ in range(2)]
    pass_numbers = [random.choice(numbers) for _ in range(2)]

    password_list = pass_letters + pass_symbols + pass_numbers
    random.shuffle(password_list)

    return "".join(password_list)


# ---------------------------- UI INTERFACE FUNCTIONS ------------------------------- #
def handle_password_generation():
    """یہ فنکشن صرف بٹن کلک اور اسکرین (UI) پر پاس ورڈ دکھانے کو سنبھالتا ہے"""
    # الگ فنکشن کو کال کر کے پاس ورڈ حاصل کرنا
    generated_password = create_secure_string(length=14)

    # اسکرین پر موجود باکس کو صاف کر کے نیا پاس ورڈ لکھنا
    entry_password.delete(0, tk.END)
    entry_password.insert(0, generated_password)

    # کی بورڈ کلپ بورڈ پر خود بخود کاپی کرنا
    root.clipboard_clear()
    root.clipboard_append(generated_password)


def save():
    website = entry_website.get().strip().title()
    email = entry_email.get().strip()
    password = entry_password.get().strip()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except (FileNotFoundError, json.JSONDecodeError):
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            entry_website.delete(0, tk.END)
            entry_password.delete(0, tk.END)
            messagebox.showinfo(title="Success", message="Details saved successfully!")


def find_password():
    website = entry_website.get().strip().title()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showerror(title="Error", message=f"No details for {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #
root = tk.Tk()
root.title("Secure Password Manager")
root.config(padx=40, pady=40, bg="#f4f6f9")
root.geometry("550x350")

# Labels
label_website = tk.Label(root, text="Website:", font=("Helvetica", 10, "bold"), bg="#f4f6f9", fg="#2d3748")
label_website.grid(row=1, column=0, sticky="W", pady=8)

label_email = tk.Label(root, text="Email/Username:", font=("Helvetica", 10, "bold"), bg="#f4f6f9", fg="#2d3748")
label_email.grid(row=2, column=0, sticky="W", pady=8)

label_password = tk.Label(root, text="Password:", font=("Helvetica", 10, "bold"), bg="#f4f6f9", fg="#2d3748")
label_password.grid(row=3, column=0, sticky="W", pady=8)

# Entries
entry_website = tk.Entry(root, width=24, font=("Helvetica", 11), bd=1, relief="solid")
entry_website.grid(row=1, column=1, sticky="W", pady=8)
entry_website.focus()

entry_email = tk.Entry(root, width=42, font=("Helvetica", 11), bd=1, relief="solid")
entry_email.grid(row=2, column=1, columnspan=2, sticky="W", pady=8)
entry_email.insert(0, "your_email@gmail.com")

entry_password = tk.Entry(root, width=24, font=("Helvetica", 11), bd=1, relief="solid")
entry_password.grid(row=3, column=1, sticky="W", pady=8)

# Buttons
btn_search = tk.Button(root, text="Search", width=14, font=("Helvetica", 9, "bold"), bg="#1a365d", fg="white", bd=0,
                       command=find_password)
btn_search.grid(row=1, column=2, sticky="W", padx=5)

# یہاں کمانڈ میں نئے ہینڈلر فنکشن کو کال کیا گیا ہے
btn_generate = tk.Button(root, text="Generate Password", width=14, font=("Helvetica", 9, "bold"), bg="#2b6cb0",
                         fg="white", bd=0, command=handle_password_generation)
btn_generate.grid(row=3, column=2, sticky="W", padx=5)

btn_add = tk.Button(root, text="Add / Save Password", width=48, font=("Helvetica", 10, "bold"), bg="#4caf50",
                    fg="white", bd=0, pady=5, command=save)
btn_add.grid(row=4, column=1, columnspan=2, sticky="W", pady=15)

root.mainloop()
