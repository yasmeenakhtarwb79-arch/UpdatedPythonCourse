import tkinter as tk
import json
import os
from datetime import date

# --- 1. میموری اور ڈیٹا ہینڈلنگ ---
DATA_FILE = "habits_data.txt"  # اب یہ ایک سادہ ٹیکسٹ فائل بنے گی
TODAY = str(date.today())

# عادات کے نام (بغیر کسی پائتھون یونی کوڈ ایرر کے)
DEFAULT_HABITS = {
    "Coding": {"history": {}, "streak": 0},
    "Exercise": {"history": {}, "streak": 0},
    "Reading": {"history": {}, "streak": 0}
}

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return DEFAULT_HABITS
    return DEFAULT_HABITS

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- 2. انٹرفیس (UI) کا سیٹ اپ ---
class HabitTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My Habit Tracker")
        self.root.geometry("400x350")
        self.root.configure(bg="#1e1e2e")  # ڈارک تھیم رینگز

        self.habits = load_data()

        # ہیڈر (آج کی تاریخ)
        header_text = f"Date: {TODAY}"
        header = tk.Label(root, text=header_text, font=("Arial", 16, "bold"), fg="#cdd6f4", bg="#1e1e2e")
        header.pack(pady=20)

        self.streak_labels = {}
        self.check_vars = {}

        # عادات کی لسٹ بنانا
        for habit_name, habit_info in self.habits.items():
            frame = tk.Frame(root, bg="#313244", bd=2, relief="groove")
            frame.pack(fill="x", padx=20, pady=5)

            # عادت کا نام
            lbl_name = tk.Label(frame, text=habit_name, font=("Arial", 12, "bold"), fg="#cdd6f4", bg="#313244", width=12, anchor="w")
            lbl_name.pack(side="left", padx=10, pady=10)

            # اسٹریک کا کاؤنٹر
            current_streak = habit_info.get("streak", 0)
            lbl_streak = tk.Label(frame, text=f"Streak: {current_streak}", font=("Arial", 11), fg="#fab387", bg="#313244")
            lbl_streak.pack(side="left", padx=10)
            self.streak_labels[habit_name] = lbl_streak

            # چیک باکس
            is_done = habit_info["history"].get(TODAY, False)
            var = tk.BooleanVar(value=is_done)
            self.check_vars[habit_name] = var

            chk = tk.Checkbutton(
                frame,
                variable=var,
                bg="#313244",
                activebackground="#313244",
                selectcolor="#1e1e2e",
                command=lambda name=habit_name: self.toggle_habit(name)
            )
            chk.pack(side="right", padx=10)

    # --- 3. ٹریکنگ لاجک ---
    def toggle_habit(self, habit_name):
        is_checked = self.check_vars[habit_name].get()
        history = self.habits[habit_name]["history"]

        if is_checked:
            history[TODAY] = True
            self.habits[habit_name]["streak"] += 1
        else:
            history[TODAY] = False
            if self.habits[habit_name]["streak"] > 0:
                self.habits[habit_name]["streak"] -= 1

        # ڈیٹا سیو کریں اور لیبل اپڈیٹ کریں
        save_data(self.habits)
        self.streak_labels[habit_name].config(text=f"Streak: {self.habits[habit_name]['streak']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HabitTrackerApp(root)
    root.mainloop()
