import tkinter as tk
from tkinter import ttk


class PomodoroApp:
	WORK_MINUTES = 25
	SHORT_BREAK_MINUTES = 5
	LONG_BREAK_MINUTES = 15
	SESSIONS_PER_LONG_BREAK = 4

	def __init__(self, root):
		self.root = root
		self.root.title("Pomodoro Timer")
		self.root.resizable(False, False)

		self.mode = "Work"
		self.remaining_seconds = self.WORK_MINUTES * 60
		self.completed_sessions = 0
		self.running = False
		self.after_id = None

		frame = ttk.Frame(root, padding=24)
		frame.pack()

		self.mode_label = ttk.Label(frame, text=self.mode, font=("Arial", 18, "bold"))
		self.mode_label.pack(pady=(0, 8))
		self.clock_label = ttk.Label(frame, font=("Arial", 48, "bold"))
		self.clock_label.pack(pady=4)
		self.sessions_label = ttk.Label(frame, text="Completed sessions: 0")
		self.sessions_label.pack(pady=(4, 16))

		controls = ttk.Frame(frame)
		controls.pack()
		self.start_button = ttk.Button(controls, text="Start", command=self.toggle_timer)
		self.start_button.grid(row=0, column=0, padx=5)
		ttk.Button(controls, text="Reset", command=self.reset_timer).grid(row=0, column=1, padx=5)

		self.update_display()

	def toggle_timer(self):
		if self.running:
			self.pause_timer()
			return
		self.running = True
		self.start_button.config(text="Pause")
		self.tick()

	def tick(self):
		if not self.running:
			return
		if self.remaining_seconds <= 0:
			self.finish_period()
			return
		self.remaining_seconds -= 1
		self.update_display()
		if self.remaining_seconds == 0:
			self.finish_period()
		else:
			self.after_id = self.root.after(1000, self.tick)

	def finish_period(self):
		self.running = False
		self.after_id = None
		self.start_button.config(text="Start")
		if self.mode == "Work":
			self.completed_sessions += 1
			if self.completed_sessions % self.SESSIONS_PER_LONG_BREAK == 0:
				self.set_period("Long break", self.LONG_BREAK_MINUTES)
			else:
				self.set_period("Short break", self.SHORT_BREAK_MINUTES)
		else:
			self.set_period("Work", self.WORK_MINUTES)
		self.root.bell()

	def set_period(self, mode, minutes):
		self.mode = mode
		self.remaining_seconds = minutes * 60
		self.update_display()

	def pause_timer(self):
		self.running = False
		self.start_button.config(text="Start")
		if self.after_id is not None:
			self.root.after_cancel(self.after_id)
			self.after_id = None

	def reset_timer(self):
		self.pause_timer()
		self.mode = "Work"
		self.remaining_seconds = self.WORK_MINUTES * 60
		self.update_display()

	def update_display(self):
		minutes, seconds = divmod(self.remaining_seconds, 60)
		self.clock_label.config(text=f"{minutes:02d}:{seconds:02d}")
		self.mode_label.config(text=self.mode)
		self.sessions_label.config(text=f"Completed sessions: {self.completed_sessions}")
		self.root.title(f"{minutes:02d}:{seconds:02d} — Pomodoro Timer")


if __name__ == "__main__":
	window = tk.Tk()
	PomodoroApp(window)
	window.mainloop()
