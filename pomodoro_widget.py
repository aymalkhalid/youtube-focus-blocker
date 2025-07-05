import tkinter as tk
from tkinter import messagebox
import os

class PomodoroWidget(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, bg="#232946", *args, **kwargs)
        self.pomo_label = tk.Label(self, text="Pomodoro Timer", bg="#232946", fg="#eebbc3", font=("Segoe UI", 11, "bold"))
        self.pomo_label.grid(row=0, column=0, columnspan=2, pady=(0, 5))
        self.pomo_time_var = tk.StringVar(value="25:00")
        self.pomo_time_display = tk.Label(self, textvariable=self.pomo_time_var, bg="#232946", fg="#fffffe", font=("Segoe UI", 16, "bold"))
        self.pomo_time_display.grid(row=1, column=0, columnspan=2)
        self.pomo_start_btn = tk.Button(self, text="Start Focus", command=self.start_pomodoro, bg="#eebbc3", fg="#232946", font=("Segoe UI", 10, "bold"), width=10)
        self.pomo_start_btn.grid(row=2, column=0, pady=5, padx=5)
        self.pomo_reset_btn = tk.Button(self, text="Reset", command=self.reset_pomodoro, bg="#eebbc3", fg="#232946", font=("Segoe UI", 10), width=10)
        self.pomo_reset_btn.grid(row=2, column=1, pady=5, padx=5)
        self.pomo_running = False
        self.pomo_seconds_left = 25 * 60
        self.pomo_on_break = False

    def start_pomodoro(self):
        if not self.pomo_running:
            self.pomo_running = True
            self.pomo_start_btn.config(text="Pause", command=self.pause_pomodoro)
            self.run_pomodoro()
        else:
            self.pause_pomodoro()

    def pause_pomodoro(self):
        self.pomo_running = False
        self.pomo_start_btn.config(text="Resume", command=self.start_pomodoro)

    def reset_pomodoro(self):
        self.pomo_running = False
        self.pomo_on_break = False
        self.pomo_seconds_left = 25 * 60
        self.pomo_time_var.set("25:00")
        self.pomo_start_btn.config(text="Start Focus", command=self.start_pomodoro)

    def run_pomodoro(self):
        if self.pomo_running:
            if self.pomo_seconds_left > 0:
                mins, secs = divmod(self.pomo_seconds_left, 60)
                self.pomo_time_var.set(f"{mins:02d}:{secs:02d}")
                self.pomo_seconds_left -= 1
                self.after(1000, self.run_pomodoro)
            else:
                self.pomo_running = False
                if not self.pomo_on_break:
                    self.pomo_on_break = True
                    self.pomo_seconds_left = 5 * 60
                    self.pomo_time_var.set("05:00")
                    self.pomo_start_btn.config(text="Start Break", command=self.start_pomodoro)
                    self.show_pomodoro_alert("Focus session complete! Time for a break.")
                else:
                    self.pomo_on_break = False
                    self.pomo_seconds_left = 25 * 60
                    self.pomo_time_var.set("25:00")
                    self.pomo_start_btn.config(text="Start Focus", command=self.start_pomodoro)
                    self.show_pomodoro_alert("Break over! Back to focus.")

    def show_pomodoro_alert(self, message, sound_file=None):
        # Play custom sound if provided, else default beep
        try:
            import winsound
            if sound_file and os.path.exists(sound_file):
                winsound.PlaySound(sound_file, winsound.SND_FILENAME | winsound.SND_ASYNC)
            else:
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        except Exception:
            pass
        # Visual flash effect
        self.flash_bg()
        # Non-blocking popup
        self.non_blocking_popup(message)

    def flash_bg(self):
        original = self["bg"]
        def flash(count=0):
            if count < 6:
                color = "#eebbc3" if count % 2 == 0 else original
                self.configure(bg=color)
                self.after(120, lambda: flash(count+1))
            else:
                self.configure(bg=original)
        flash()

    def non_blocking_popup(self, message):
        popup = tk.Toplevel(self)
        popup.title("Pomodoro Timer Alert")
        popup.geometry("300x100")
        popup.configure(bg="#232946")
        label = tk.Label(popup, text=message, bg="#232946", fg="#eebbc3", font=("Segoe UI", 11, "bold"))
        label.pack(expand=True, fill="both", padx=10, pady=10)
        popup.after(3500, popup.destroy)
