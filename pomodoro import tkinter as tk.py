import tkinter as tk
from tkinter import ttk


class PomodoroTimer:
    WORK_SECONDS = 25 * 60
    BREAK_SECONDS = 5 * 60

    def __init__(self, root):
        self.root = root
        root.title("Pomodoro Timer")
        root.resizable(False, False)
        root.configure(padx=28, pady=24, bg="#f5f2eb")

        self.mode = "Work"
        self.remaining = self.WORK_SECONDS
        self.running = False
        self.after_id = None
        self.sessions = 0

        self.mode_label = tk.Label(root, text="", font=("Arial", 18, "bold"),
                                   bg="#f5f2eb", fg="#c45245")
        self.mode_label.pack(pady=(0, 4))
        self.clock_label = tk.Label(root, text="", font=("Arial", 56, "bold"),
                                    bg="#f5f2eb", fg="#303030")
        self.clock_label.pack()
        self.progress = ttk.Progressbar(root, length=280, mode="determinate")
        self.progress.pack(fill="x", pady=(8, 20))

        controls = ttk.Frame(root)
        controls.pack()
        self.start_button = ttk.Button(controls, text="Start", command=self.toggle)
        self.start_button.pack(side="left", padx=4)
        ttk.Button(controls, text="Reset", command=self.reset).pack(side="left", padx=4)
        ttk.Button(controls, text="Skip", command=self.skip).pack(side="left", padx=4)

        self.sessions_label = tk.Label(root, text="Completed work sessions: 0",
                                       font=("Arial", 10), bg="#f5f2eb", fg="#666666")
        self.sessions_label.pack(pady=(18, 0))
        self.update_display()

    def toggle(self):
        self.running = not self.running
        self.start_button.configure(text="Pause" if self.running else "Start")
        if self.running:
            self.tick()
        elif self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def tick(self):
        self.after_id = None
        if not self.running:
            return
        if self.remaining > 0:
            self.remaining -= 1
            self.update_display()
            self.after_id = self.root.after(1000, self.tick)
        else:
            self.root.bell()
            self.change_mode()
            self.tick()

    def change_mode(self):
        if self.mode == "Work":
            self.sessions += 1
            self.mode = "Break"
            self.remaining = self.BREAK_SECONDS
        else:
            self.mode = "Work"
            self.remaining = self.WORK_SECONDS
        self.update_display()

    def stop_timer(self):
        self.running = False
        self.start_button.configure(text="Start")
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def reset(self):
        self.stop_timer()
        self.mode = "Work"
        self.remaining = self.WORK_SECONDS
        self.update_display()

    def skip(self):
        self.stop_timer()
        self.change_mode()

    def update_display(self):
        minutes, seconds = divmod(self.remaining, 60)
        self.clock_label.configure(text=f"{minutes:02d}:{seconds:02d}")
        self.mode_label.configure(
            text=self.mode,
            fg="#c45245" if self.mode == "Work" else "#438765",
        )
        duration = self.WORK_SECONDS if self.mode == "Work" else self.BREAK_SECONDS
        self.progress.configure(maximum=duration, value=duration - self.remaining)
        self.sessions_label.configure(text=f"Completed work sessions: {self.sessions}")


if __name__ == "__main__":
    app_root = tk.Tk()
    PomodoroTimer(app_root)
    app_root.mainloop()