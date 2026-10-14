import tkinter as tk
from tkinter import messagebox
import random
import html
import requests
from urllib.parse import unquote

# ---------------- SETTINGS ----------------
API_URL = "https://opentdb.com/api.php"
QUESTION_COUNT = 10
CATEGORY = 18          # Science: Computers
DIFFICULTY = "easy"    # easy, medium, hard
REQUEST_TIMEOUT = 15

BG = "#101216"
PANEL = "#191d24"
CARD = "#222833"
TEXT = "#f4f6fa"
MUTED = "#aab2c0"
ACCENT = "#e8b84a"
GREEN = "#65d69a"
RED = "#ff7777"


class CyberQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WILL | Computer Security Quiz")
        self.root.geometry("850x650")
        self.root.minsize(700, 560)
        self.root.configure(bg=BG)

        self.questions = []
        self.question_index = 0
        self.score = 0
        self.answered = False
        self.choice = tk.StringVar(value="")

        self.build_ui()
        self.load_questions()

    def build_ui(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=28, pady=(22, 10))

        tk.Label(
            header, text="CYBER / COMPUTER QUIZ",
            font=("Segoe UI", 21, "bold"), bg=BG, fg=ACCENT
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Powered by Open Trivia Database • No API key required",
            font=("Segoe UI", 10), bg=BG, fg=MUTED
        ).pack(anchor="w", pady=(4, 0))

        self.status_label = tk.Label(
            self.root, text="Connecting to question database...",
            font=("Segoe UI", 11), bg=BG, fg=MUTED
        )
        self.status_label.pack(anchor="w", padx=30, pady=(8, 10))

        self.card = tk.Frame(self.root, bg=PANEL, padx=24, pady=22)
        self.card.pack(fill="both", expand=True, padx=28, pady=(0, 18))

        self.progress_label = tk.Label(
            self.card, text="", font=("Segoe UI", 10, "bold"),
            bg=PANEL, fg=ACCENT
        )
        self.progress_label.pack(anchor="w")

        self.question_label = tk.Label(
            self.card, text="Loading questions...",
            font=("Segoe UI", 15, "bold"), bg=PANEL, fg=TEXT,
            wraplength=740, justify="left", anchor="w"
        )
        self.question_label.pack(fill="x", anchor="w", pady=(18, 20))

        self.options_frame = tk.Frame(self.card, bg=PANEL)
        self.options_frame.pack(fill="x", anchor="w")

        self.feedback_label = tk.Label(
            self.card, text="", font=("Segoe UI", 11),
            bg=PANEL, fg=MUTED, wraplength=740, justify="left",
            anchor="w"
        )
        self.feedback_label.pack(fill="x", anchor="w", pady=(18, 0))

        footer = tk.Frame(self.root, bg=BG)
        footer.pack(fill="x", padx=28, pady=(0, 22))

        self.score_label = tk.Label(
            footer, text="Score: 0", font=("Segoe UI", 11, "bold"),
            bg=BG, fg=TEXT
        )
        self.score_label.pack(side="left")

        self.action_button = tk.Button(
            footer, text="CHECK ANSWER", command=self.check_answer,
            font=("Segoe UI", 10, "bold"), bg=ACCENT, fg="#151515",
            activebackground="#f5cf71", relief="flat", padx=22, pady=11,
            cursor="hand2"
        )
        self.action_button.pack(side="right")

        self.reload_button = tk.Button(
            footer, text="NEW QUIZ", command=self.load_questions,
            font=("Segoe UI", 10, "bold"), bg=CARD, fg=TEXT,
            activebackground=PANEL, relief="flat", padx=18, pady=11,
            cursor="hand2"
        )
        self.reload_button.pack(side="right", padx=(0, 10))

    def load_questions(self):
        self.action_button.config(state="disabled", text="LOADING...")
        self.reload_button.config(state="disabled")
        self.status_label.config(text="Downloading questions from OpenTDB...", fg=MUTED)
        self.question_label.config(text="Please wait while questions load.")
        self.feedback_label.config(text="")
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        self.root.update_idletasks()

        try:
            response = requests.get(
                API_URL,
                params={
                    "amount": QUESTION_COUNT,
                    "category": CATEGORY,
                    "difficulty": DIFFICULTY,
                    "type": "multiple",
                    "encode": "url3986",
                },
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            payload = response.json()

            if payload.get("response_code") != 0:
                messages = {
                    1: "Not enough questions for these settings. Try fewer questions or another difficulty.",
                    2: "The API request contains an invalid parameter.",
                    3: "The API session token was not found.",
                    4: "The API question pool needs to be refreshed. Please try again.",
                    5: "The API is rate-limiting requests. Wait a little and try again.",
                }
                raise ValueError(messages.get(payload.get("response_code"),
                                              "OpenTDB returned an unknown error."))

            results = payload.get("results", [])
            if not results:
                raise ValueError("The API returned no questions.")

            self.questions = []
            for item in results:
                question = self.decode_text(item.get("question", ""))
                correct = self.decode_text(item.get("correct_answer", ""))
                incorrect = [self.decode_text(x) for x in item.get("incorrect_answers", [])]
                options = incorrect + [correct]
                random.shuffle(options)
                self.questions.append({
                    "question": question,
                    "correct": correct,
                    "options": options,
                    "category": self.decode_text(item.get("category", "Computers")),
                })

            self.question_index = 0
            self.score = 0
            self.score_label.config(text="Score: 0")
            self.status_label.config(
                text=f"Loaded {len(self.questions)} questions • Computer Science",
                fg=GREEN
            )
            self.show_question()

        except requests.exceptions.Timeout:
            self.show_error("The request timed out. Check your internet and click NEW QUIZ.")
        except requests.exceptions.SSLError:
            self.show_error("Secure connection failed. Check your date/time and internet connection.")
        except requests.exceptions.RequestException as exc:
            self.show_error(f"Could not connect to OpenTDB.\n{exc}")
        except (ValueError, KeyError, TypeError) as exc:
            self.show_error(str(exc))
        finally:
            self.reload_button.config(state="normal")

    @staticmethod
    def decode_text(value):
        # OpenTDB uses URL3986 encoding, so unquote the text and then decode HTML entities.
        return html.unescape(unquote(str(value)))

    def show_error(self, message):
        self.questions = []
        self.status_label.config(text="Questions could not be loaded.", fg=RED)
        self.question_label.config(text="Unable to load quiz questions.")
        self.feedback_label.config(text=message, fg=RED)
        self.action_button.config(state="disabled", text="CHECK ANSWER")

    def show_question(self):
        self.answered = False
        self.choice.set("")
        self.feedback_label.config(text="", fg=MUTED)
        question = self.questions[self.question_index]

        self.progress_label.config(
            text=f"QUESTION {self.question_index + 1} OF {len(self.questions)}"
        )
        self.question_label.config(text=question["question"])

        for widget in self.options_frame.winfo_children():
            widget.destroy()

        for index, option in enumerate(question["options"]):
            radio = tk.Radiobutton(
                self.options_frame,
                text=option,
                variable=self.choice,
                value=option,
                font=("Segoe UI", 11),
                bg=PANEL, fg=TEXT, selectcolor=CARD,
                activebackground=PANEL, activeforeground=ACCENT,
                anchor="w", justify="left", wraplength=710,
                padx=12, pady=10, cursor="hand2"
            )
            radio.pack(fill="x", anchor="w", pady=3)

        self.score_label.config(text=f"Score: {self.score}")
        self.action_button.config(state="normal", text="CHECK ANSWER")

    def check_answer(self):
        if not self.questions:
            return

        if self.answered:
            if self.question_index < len(self.questions) - 1:
                self.question_index += 1
                self.show_question()
            else:
                self.show_results()
            return

        selected = self.choice.get()
        if not selected:
            messagebox.showinfo("Choose an answer", "Please select an option first.")
            return

        self.answered = True
        correct = self.questions[self.question_index]["correct"]

        if selected == correct:
            self.score += 1
            self.feedback_label.config(text="Correct! Great work.", fg=GREEN)
        else:
            self.feedback_label.config(text=f"Not quite. Correct answer: {correct}", fg=RED)

        self.score_label.config(text=f"Score: {self.score}")
        self.action_button.config(
            text="NEXT QUESTION" if self.question_index < len(self.questions) - 1
            else "SHOW RESULTS"
        )

    def show_results(self):
        total = len(self.questions)
        percent = round((self.score / total) * 100) if total else 0
        self.progress_label.config(text="QUIZ COMPLETE")
        self.question_label.config(text=f"You scored {self.score} out of {total} ({percent}%).")
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        self.feedback_label.config(
            text="Excellent work!" if percent >= 80 else
                 "Good effort! Try another round to practise more.",
            fg=GREEN if percent >= 80 else MUTED
        )
        self.action_button.config(text="PLAY AGAIN", state="normal", command=self.load_questions)
        self.status_label.config(text="Quiz finished • Select NEW QUIZ or PLAY AGAIN", fg=ACCENT)


if __name__ == "__main__":
    root = tk.Tk()
    app = CyberQuizApp(root)
    root.mainloop()
