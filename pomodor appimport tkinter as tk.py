import tkinter as tk
from tkinter import messagebox


class PomodoroApp:
    WORK_MINUTES = 25
    SHORT_BREAK_MINUTES = 5
    LONG_BREAK_MINUTES = 15
    SESSIONS_BEFORE_LONG_BREAK = 4

    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.resizable(False, False)
        self.root.configure(bg="#f7f3ed")
        self.running = False
        self.after_id = None
        self.mode = "Work"
        self.sessions_completed = 0
        self.remaining_seconds = self.WORK_MINUTES * 60
        self.focus_window = None
        self.focus_timer_label = None
        self.focus_mode_label = None

        self.mode_label = tk.Label(root, text="WORK", font=("Helvetica", 14, "bold"),
                                   bg="#f7f3ed", fg="#d9534f")
        self.mode_label.pack(pady=(24, 4))
        self.timer_label = tk.Label(root, text="25:00", font=("Helvetica", 56, "bold"),
                                    bg="#f7f3ed", fg="#333333")
        self.timer_label.pack(padx=36, pady=8)
        self.progress_label = tk.Label(root, text="Sessions completed: 0",
                                        font=("Helvetica", 11), bg="#f7f3ed", fg="#666666")
        self.progress_label.pack(pady=(0, 16))

        controls = tk.Frame(root, bg="#f7f3ed")
        controls.pack(pady=(0, 24))
        self.start_button = tk.Button(
            controls, text="Start", width=10, command=self.toggle_timer,
            bg="#d9534f", fg="white", activebackground="#c94440",
            activeforeground="white", relief="flat", font=("Helvetica", 11, "bold"))
        self.start_button.pack(side="left", padx=6, ipady=6)
        tk.Button(controls, text="Reset", width=10, command=self.reset_timer,
                  bg="#e5dfd6", fg="#333333", activebackground="#d8d0c5",
                  relief="flat", font=("Helvetica", 11)).pack(side="left", padx=6, ipady=6)
        tk.Button(controls, text="Focus Screen", command=self.open_focus_window,
                  bg="#e5dfd6", fg="#333333", activebackground="#d8d0c5",
                  relief="flat", font=("Helvetica", 11)).pack(side="left", padx=6, ipady=6)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def open_focus_window(self):
        """Open a fullscreen, always-on-top timer visible above other apps."""
        if self.focus_window is not None and self.focus_window.winfo_exists():
            self.focus_window.deiconify()
            self.focus_window.focus_force()
            return

        window = tk.Toplevel(self.root)
        self.focus_window = window
        window.title("Pomodoro Focus")
        window.configure(bg="#f7f3ed")
        window.attributes("-fullscreen", True)
        window.attributes("-topmost", True)
        window.bind("<Escape>", lambda _event: self.close_focus_window())

        tk.Label(window, text="POMODORO FOCUS", font=("Helvetica", 18, "bold"),
                 bg="#f7f3ed", fg="#666666").pack(pady=(60, 12))
        self.focus_mode_label = tk.Label(
            window, font=("Helvetica", 24, "bold"), bg="#f7f3ed")
        self.focus_mode_label.pack(pady=8)
        self.focus_timer_label = tk.Label(
            window, font=("Helvetica", 100, "bold"), bg="#f7f3ed", fg="#333333")
        self.focus_timer_label.pack(pady=16)
        tk.Label(window, text="Press Esc to leave the full-screen timer",
                 font=("Helvetica", 12), bg="#f7f3ed", fg="#777777").pack(pady=12)

        buttons = tk.Frame(window, bg="#f7f3ed")
        buttons.pack(pady=24)
        tk.Button(buttons, text="Pause / Resume", command=self.toggle_timer,
                  font=("Helvetica", 12, "bold"), relief="flat",
                  padx=18, pady=10).pack(side="left", padx=8)
        tk.Button(buttons, text="Close Focus Screen", command=self.close_focus_window,
                  font=("Helvetica", 12), relief="flat",
                  padx=18, pady=10).pack(side="left", padx=8)
        window.protocol("WM_DELETE_WINDOW", self.close_focus_window)
        self.update_display()

    def close_focus_window(self):
        if self.focus_window is not None:
            window = self.focus_window
            self.focus_window = None
            self.focus_timer_label = None
            self.focus_mode_label = None
            window.destroy()

    def toggle_timer(self):
        self.running = not self.running
        self.start_button.config(text="Pause" if self.running else "Start")
        if self.running:
            self.tick()
        elif self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def tick(self):
        if not self.running:
            return
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_display()
            self.after_id = self.root.after(1000, self.tick)
            return
        self.running = False
        self.after_id = None
        self.start_button.config(text="Start")
        self.finish_session()

    def finish_session(self):
        if self.mode == "Work":
            self.sessions_completed += 1
            self.progress_label.config(text=f"Sessions completed: {self.sessions_completed}")
            if self.sessions_completed % self.SESSIONS_BEFORE_LONG_BREAK == 0:
                self.set_mode("Long Break", self.LONG_BREAK_MINUTES)
            else:
                self.set_mode("Short Break", self.SHORT_BREAK_MINUTES)
            messagebox.showinfo("Pomodoro", "Work session complete. Time for a break!")
        else:
            self.set_mode("Work", self.WORK_MINUTES)
            messagebox.showinfo("Pomodoro", "Break complete. Ready to focus?")

    def set_mode(self, mode, minutes):
        self.mode = mode
        self.remaining_seconds = minutes * 60
        color = "#d9534f" if mode == "Work" else "#4b9b83"
        self.mode_label.config(text=mode.upper(), fg=color)
        self.start_button.config(bg=color, activebackground=color)
        self.update_display()

    def reset_timer(self):
        self.running = False
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.start_button.config(text="Start")
        minutes = (self.WORK_MINUTES if self.mode == "Work" else
                   self.LONG_BREAK_MINUTES if self.mode == "Long Break" else
                   self.SHORT_BREAK_MINUTES)
        self.remaining_seconds = minutes * 60
        self.update_display()

    def update_display(self):
        minutes, seconds = divmod(self.remaining_seconds, 60)
        text = f"{minutes:02d}:{seconds:02d}"
        self.timer_label.config(text=text)
        self.root.title(f"{text} — Pomodoro Timer")
        if self.focus_window is not None and self.focus_window.winfo_exists():
            self.focus_timer_label.config(text=text)
            color = "#d9534f" if self.mode == "Work" else "#4b9b83"
            self.focus_mode_label.config(text=self.mode.upper(), fg=color)

    def close(self):
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
        self.close_focus_window()
        self.root.destroy()


if __name__ == "__main__":
    window = tk.Tk()
    PomodoroApp(window)
    window.mainloop()