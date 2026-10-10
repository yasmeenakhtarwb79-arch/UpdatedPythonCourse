import tkinter as tk
from tkinter import messagebox


KM_TO_MILES = 0.621371


def convert():
	"""Convert the entered distance using the currently selected direction."""
	try:
		distance = float(distance_entry.get().strip())
		if distance < 0:
			raise ValueError
	except ValueError:
		messagebox.showerror("Invalid distance", "Enter a non-negative number.")
		distance_entry.focus_set()
		return

	if direction.get() == "km_to_miles":
		answer = distance * KM_TO_MILES
		unit = "miles"
	else:
		answer = distance / KM_TO_MILES
		unit = "kilometers"
	result_value.set(f"{answer:,.2f}")
	result_unit.config(text=unit)


def clear():
	distance_entry.delete(0, tk.END)
	result_value.set("0.00")
	result_unit.config(text="miles" if direction.get() == "km_to_miles" else "kilometers")
	distance_entry.focus_set()


root = tk.Tk()
root.title("Distance Studio | KM ⇄ Miles")
root.geometry("440x500")
root.resizable(False, False)
root.configure(bg="#101827")

direction = tk.StringVar(value="km_to_miles")
result_value = tk.StringVar(value="0.00")

card = tk.Frame(root, bg="#1b2940", padx=30, pady=26)
card.pack(fill="both", expand=True, padx=22, pady=22)

tk.Label(card, text="DISTANCE STUDIO", bg="#1b2940", fg="#51e0c2",
		 font=("Segoe UI", 10, "bold")).pack(anchor="w")
tk.Label(card, text="Go the distance.", bg="#1b2940", fg="white",
		 font=("Segoe UI", 24, "bold")).pack(anchor="w", pady=(5, 3))
tk.Label(card, text="A stylish kilometer and mile converter", bg="#1b2940",
		 fg="#a9b7ca", font=("Segoe UI", 10)).pack(anchor="w")

tk.Label(card, text="CONVERSION", bg="#1b2940", fg="#a9b7ca",
		 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(24, 8))
choices = tk.Frame(card, bg="#1b2940")
choices.pack(fill="x")
tk.Radiobutton(choices, text="KM  →  MILES", variable=direction, value="km_to_miles",
			   command=clear, bg="#293b56", fg="white", selectcolor="#293b56",
			   activebackground="#344c6d", activeforeground="white",
			   font=("Segoe UI", 10, "bold"), padx=12, pady=11).pack(side="left", expand=True, fill="x")
tk.Radiobutton(choices, text="MILES  →  KM", variable=direction, value="miles_to_km",
			   command=clear, bg="#293b56", fg="white", selectcolor="#293b56",
			   activebackground="#344c6d", activeforeground="white",
			   font=("Segoe UI", 10, "bold"), padx=12, pady=11).pack(side="left", expand=True, fill="x", padx=(8, 0))

tk.Label(card, text="DISTANCE", bg="#1b2940", fg="#a9b7ca",
		 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(20, 7))
distance_entry = tk.Entry(card, bg="#111c2d", fg="white", insertbackground="white",
						  relief="flat", font=("Segoe UI", 18), highlightthickness=1,
						  highlightbackground="#34445c", highlightcolor="#51e0c2")
distance_entry.pack(fill="x", ipady=11)
distance_entry.bind("<Return>", lambda _event: convert())

buttons = tk.Frame(card, bg="#1b2940")
buttons.pack(fill="x", pady=(13, 20))
tk.Button(buttons, text="CONVERT", command=convert, bg="#51e0c2", fg="#10202b",
		  activebackground="#72f0d5", relief="flat", font=("Segoe UI", 10, "bold"),
		  pady=12, cursor="hand2").pack(side="left", expand=True, fill="x")
tk.Button(buttons, text="CLEAR", command=clear, bg="#293b56", fg="white",
		  activebackground="#344c6d", relief="flat", font=("Segoe UI", 10, "bold"),
		  pady=12, cursor="hand2").pack(side="left", expand=True, fill="x", padx=(8, 0))

tk.Label(card, text="YOUR RESULT", bg="#1b2940", fg="#a9b7ca",
		 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 8))
result_box = tk.Frame(card, bg="#111c2d", padx=17, pady=12)
result_box.pack(fill="x")
tk.Label(result_box, textvariable=result_value, bg="#111c2d", fg="#51e0c2",
		 font=("Segoe UI", 26, "bold")).pack(side="left")
result_unit = tk.Label(result_box, text="miles", bg="#111c2d", fg="#dbe8f5",
					   font=("Segoe UI", 11))
result_unit.pack(side="right", padx=(8, 0), pady=(9, 0))
tk.Label(card, text="Tip: Press Enter to convert", bg="#1b2940", fg="#71839b",
		 font=("Segoe UI", 9)).pack(anchor="w", pady=(15, 0))

distance_entry.focus_set()
root.mainloop()
