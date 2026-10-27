import tkinter as tk
from tkinter import messagebox
import random
import time


class FreshTypingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⌨️ SPEED TYPING CORE v5.0")
        self.root.geometry("750x550")
        self.root.configure(bg="#111424")

        self.texts = [
            "The quick brown fox jumps over the lazy dog.",
            "Python programming is easy, powerful and fun to learn.",
            "Technology works best when it brings people together successfully."
        ]

        self.time_left = 60
        self.running = False
        self.start_time = 0
        self.target_text = ""

        # Title
        tk.Label(self.root, text="⚡ CYBER TYPING TESTER", font=("Arial", 22, "bold"), fg="#00ffcc", bg="#111424").pack(
            pady=15)

        # Operator Name
        name_frame = tk.Frame(self.root, bg="#111424")
        name_frame.pack(pady=5)
        tk.Label(name_frame, text="OPERATOR NAME: ", font=("Arial", 11, "bold"), fg="#ff007f", bg="#111424").pack(
            side="left")
        self.name_entry = tk.Entry(name_frame, font=("Arial", 11), bg="#090b14", fg="#fff", bd=1, width=15)
        self.name_entry.insert(0, "Admin_User")
        self.name_entry.pack(side="left", padx=5)

        # Stats (Fixed error here)
        self.stats_lbl = tk.Label(self.root, text="Time: 60s  |  WPM: 0  |  Accuracy: 100%", font=("Arial", 14, "bold"),
                                  fg="#ffffff", bg="#090b14", pady=10, width=50)
        self.stats_lbl.pack(pady=15)

        # Display Text
        self.text_lbl = tk.Label(self.root, text="Press 'START TEST' to begin...", font=("Consolas", 13), fg="#8892b0",
                                 bg="#04050a", width=65, height=4, wraplength=550, relief="solid", bd=1)
        self.text_lbl.pack(pady=10)

        # Input Area
        self.input_area = tk.Text(self.root, font=("Consolas", 14), bg="#090b14", fg="#fff", insertbackground="#00ffcc",
                                  width=55, height=4, state="disabled", relief="solid", bd=1)
        self.input_area.bind("<KeyRelease>", self.check_live)
        self.input_area.pack(pady=10)

        # Start Button
        self.start_btn = tk.Button(self.root, text="START TEST", font=("Arial", 12, "bold"), bg="#ff007f", fg="#fff",
                                   width=15, bd=0, command=self.start_game)
        self.start_btn.pack(pady=15)

    def start_game(self):
        self.time_left = 60
        self.running = True
        self.target_text = random.choice(self.texts)
        self.text_lbl.config(text=self.target_text, fg="#00ffcc")

        self.input_area.config(state="normal")
        self.input_area.delete("1.0", tk.END)
        self.input_area.focus()

        self.start_time = time.time()
        self.start_btn.config(text="RESTART")
        self.countdown()

    def countdown(self):
        if self.running and self.time_left > 0:
            self.time_left -= 1
            self.update_timer_display()
            self.root.after(1000, self.countdown)
        elif self.time_left == 0:
            self.stop_game()

    def check_live(self, event):
        if not self.running: return
        user_text = self.input_area.get("1.0", "end-1c")

        time_passed = max(1, time.time() - self.start_time)
        words = len(user_text.split())
        wpm = round((words / time_passed) * 60)

        correct = sum(1 for u, t in zip(user_text, self.target_text) if u == t)
        acc = round((correct / len(user_text)) * 100) if len(user_text) > 0 else 100

        self.stats_lbl.config(text=f"Time: {self.time_left}s  |  WPM: {wpm}  |  Accuracy: {acc}%")

        if user_text == self.target_text:
            self.stop_game()

    def update_timer_display(self):
        current_text = self.stats_lbl.cget("text")
        try:
            parts = current_text.split("|")
            wpm_part = parts[1]
            acc_part = parts[2]
            self.stats_lbl.config(text=f"Time: {self.time_left}s  |{wpm_part}|{acc_part}")
        except:
            self.stats_lbl.config(text=f"Time: {self.time_left}s  |  WPM: 0  |  Accuracy: 100%")

    def stop_game(self):
        self.running = False
        self.input_area.config(state="disabled")
        self.start_btn.config(text="START TEST")
        messagebox.showinfo("Done!", "Test Completed! Show this score to your Dad!")


if __name__ == "__main__":
    root = tk.Tk()
    app = FreshTypingApp(root)
    root.mainloop()
