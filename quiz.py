import sys
import os
import tkinter as tk
from tkinter import messagebox

TIME_LIMIT = 15

def resource_path(filename):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, filename)


def load_questions():
    questions = []
    with open(resource_path("questions.txt"), "r") as file:
        for line in file:
            q, opts, ans = line.strip().split("|")
            questions.append({
                "question": q,
                "options": opts.split(","),
                "answer": ans
            })
    return questions


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MCQs Quiz App V3")
        self.root.geometry("550x500")
        self.root.config(bg="#f0f0f0")

        self.quiz_data = load_questions()
        self.q_no = 0
        self.score = 0
        self.time_left = TIME_LIMIT

        self.timer_label = tk.Label(root, font=("Arial", 12), bg="#f0f0f0")
        self.timer_label.pack(pady=5)

        self.question_label = tk.Label(root, font=("Arial", 16, "bold"),
                                       wraplength=500, bg="#f0f0f0")
        self.question_label.pack(pady=20)

        self.var = tk.StringVar()
        self.options = []

        for i in range(4):
            rb = tk.Radiobutton(root, text="", variable=self.var, value="",
                                font=("Arial", 13), bg="#f0f0f0")
            rb.pack(anchor="w", padx=60, pady=5)
            self.options.append(rb)

        self.feedback_label = tk.Label(root, text="", font=("Arial", 12, "bold"),
                                       bg="#f0f0f0")
        self.feedback_label.pack(pady=10)

        self.next_button = tk.Button(root, text="Next", width=15,
                                     command=self.next_question, bg="#4CAF50", fg="white")
        self.next_button.pack(pady=10)

        self.restart_button = tk.Button(root, text="Restart Quiz", width=15,
                                        command=self.restart_quiz, bg="#2196F3", fg="white")
        self.restart_button.pack(pady=5)

        self.load_question()
        self.start_timer()

    def load_question(self):
        self.var.set("")
        self.feedback_label.config(text="")
        self.time_left = TIME_LIMIT

        q = self.quiz_data[self.q_no]
        self.question_label.config(text=q["question"])

        for i, option in enumerate(q["options"]):
            self.options[i].config(text=option, value=option)

    def start_timer(self):
        self.timer_label.config(text=f"Time Left: {self.time_left}s")
        if self.time_left > 0:
            self.time_left -= 1
            self.root.after(1000, self.start_timer)
        else:
            self.check_answer()

    def check_answer(self):
        selected = self.var.get()
        correct = self.quiz_data[self.q_no]["answer"]

        if selected == correct:
            self.score += 1
            self.feedback_label.config(text="Correct ✅", fg="green")
        else:
            self.feedback_label.config(
                text=f"Wrong ❌  Correct: {correct}", fg="red")

        self.root.after(1500, self.next_question)

    def next_question(self):
        if self.var.get() != "":
            self.check_answer()
            return

        self.q_no += 1

        if self.q_no < len(self.quiz_data):
            self.load_question()
        else:
            self.show_result()

    def show_result(self):
        percent = int((self.score / len(self.quiz_data)) * 100)
        self.question_label.config(
            text=f"Quiz Finished!\n\nScore: {self.score}/{len(self.quiz_data)}\nPercentage: {percent}%")
        self.timer_label.config(text="")
        self.feedback_label.config(text="")
        for rb in self.options:
            rb.pack_forget()
        self.next_button.pack_forget()

    def restart_quiz(self):
        self.q_no = 0
        self.score = 0
        for rb in self.options:
            rb.pack(anchor="w", padx=60, pady=5)
        self.next_button.pack(pady=10)
        self.load_question()
        self.start_timer()


root = tk.Tk()
app = QuizApp(root)
root.mainloop()
