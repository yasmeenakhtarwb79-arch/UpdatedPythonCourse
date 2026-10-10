import tkinter as tk
from tkinter import messagebox
import random
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Arial"
current_card = {}
to_learn = []

# ---------------------------- DATA LOADING ------------------------------- #
try:
    # اگر صارف پہلے سے کچھ الفاظ سیکھ رہا ہے تو وہ فائل لوڈ کریں
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    # اگر فائل موجود نہیں ہے، تو یہ بنیادی ڈکشنری استعمال کرے گا
    fallback_data = {
        "English": ["Accomplished", "Resilient", "Strategic", "Innovative", "Competent", "Efficient", "Trustworthy"],
        "Urdu": ["ماہر", "مستحکم", "دور اندیش", "جدت پسند", "باصلاحیت", "مستعد", "قابل اعتماد"]
    }
    to_learn = pd.DataFrame(fallback_data).to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# ---------------------------- TIMER & FLIP LOGIC ------------------------------- #
def next_card():
    global current_card, flip_timer
    root.after_cancel(flip_timer)

    if len(to_learn) == 0:
        messagebox.showinfo(title="Congratulations!", message="You have learned all the words!")
        root.destroy()
        return

    current_card = random.choice(to_learn)

    # کارڈ کی سامنے والی سائیڈ (English Word)
    canvas.itemconfig(card_background, fill="white")
    canvas.itemconfig(card_title, text="English", fill="black")
    canvas.itemconfig(card_word, text=current_card["English"], fill="black")

    # 3 سیکنڈ (3000ms) بعد کارڈ پلٹنے کا ٹائمر شروع کریں
    flip_timer = root.after(3000, func=flip_card)


def flip_card():
    # کارڈ کی پیچھے والی سائیڈ (Urdu Translation)
    canvas.itemconfig(card_background, fill="#2c3e50")
    canvas.itemconfig(card_title, text="Urdu", fill="white")
    canvas.itemconfig(card_word, text=current_card["Urdu"], fill="white")


def is_known():
    # اگر صارف لفظ جانتا ہے، تو اسے لسٹ سے نکال دیں اور فائل اپڈیٹ کریں
    to_learn.remove(current_card)
    new_data = pd.DataFrame(to_learn)
    new_data.to_csv("words_to_learn.csv", index=False)
    next_card()


# ---------------------------- UI SETUP ------------------------------- #
root = tk.Tk()
root.title("Capstone Flashcard Learning App")
root.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
root.geometry("700x550")

# پہلی بار چلنے پر ٹائمر سیٹ کرنا
flip_timer = root.after(3000, func=flip_card)

# Flashcard Area (Canvas)
canvas = tk.Canvas(width=600, height=350, bg=BACKGROUND_COLOR, highlightthickness=0)
# خوبصورت راؤنڈ کارڈ بنانے کے لیے rectangle کا استعمال
card_background = canvas.create_rectangle(10, 10, 590, 340, fill="white", outline="", width=0)
card_title = canvas.create_text(300, 100, text="", font=(FONT_NAME, 24, "italic"))
card_word = canvas.create_text(300, 180, text="", font=(FONT_NAME, 40, "bold"))
canvas.pack(pady=20)

# Buttons Framework
button_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
button_frame.pack()

# Wrong / Unknown Button
unknown_button = tk.Button(
    button_frame, text="❌ Wrong", font=(FONT_NAME, 14, "bold"),
    bg="#e74c3c", fg="white", padx=20, pady=10, bd=0, cursor="hand2", command=next_card
)
unknown_button.grid(row=0, column=0, padx=40)

# Right / Known Button
known_button = tk.Button(
    button_frame, text="✅ Right", font=(FONT_NAME, 14, "bold"),
    bg="#2ecc71", fg="white", padx=20, pady=10, bd=0, cursor="hand2", command=is_known
)
known_button.grid(row=0, column=1, padx=40)

# پہلا کارڈ دکھائیں
next_card()

root.mainloop()
