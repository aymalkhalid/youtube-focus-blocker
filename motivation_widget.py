import tkinter as tk
from tkinter import messagebox
import random

class MotivationWidget(tk.Label):
    def __init__(self, master, *args, **kwargs):
        self.motivation_lines = [
            "Stay focused, your goals are within reach!",
            "Every minute counts. Make it productive!",
            "Small steps every day lead to big results.",
            "Discipline is the bridge between goals and accomplishment.",
            "You are stronger than your distractions!",
            "Progress, not perfection.",
            "Your future self will thank you for this moment!",
            "Great things never come from comfort zones.",
            "Success is the sum of small efforts repeated day in and day out.",
            "Focus on being productive instead of busy."
        ]
        super().__init__(master, text=random.choice(self.motivation_lines), *args, **kwargs)
        self.update_motivation_line()

    def update_motivation_line(self):
        self.config(text=random.choice(self.motivation_lines))
        # Change message every 5-10 seconds randomly
        interval = random.randint(5000, 10000)  # milliseconds
        self.after(interval, self.update_motivation_line)
