import tkinter as tk
from tkinter import messagebox
import time
import math

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")

        # Timer settings (in seconds)
        self.work_time = 25 * 60
        self.short_break = 5 * 60
        self.long_break = 15 * 60
        self.reps = 0

        # Timer text
        self.timer_text = tk.StringVar()
        self.timer_text.set("25:00")

        # Timer label
        self.label = tk.Label(root, text="Timer", font=("Helvetica", 24))
        self.label.pack(pady=10)

        # Timer display
        self.timer_label = tk.Label(root, textvariable=self.timer_text, font=("Helvetica", 48))
        self.timer_label.pack()

        # Start and reset buttons
        self.start_button = tk.Button(root, text="Start", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=20, pady=20)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side=tk.RIGHT, padx=20, pady=20)

        self.stop_button = tk.Button(root,text="Stop",command=self.stop_timer)
        self.stop_button.pack(side=tk.BOTTOM,padx=20,pady=20)
        # Variable to keep track of the timer
        self.timer_running = False
        self.current_time = self.work_time
        self.countdown_id = None

        # Create analog clock
        self.analog_clock = AnalogClock(root)
        self.analog_clock.pack(pady=20)

        # Update the clock every second
        self.update_clock()

    def update_clock(self):
        self.analog_clock.update_time()
        self.root.after(1000, self.update_clock)

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.reps += 1
            work_sessions = self.reps % 8
            if work_sessions == 0:
                self.current_time = self.long_break
                self.label.config(text="Long Break", fg="red")
            elif work_sessions % 2 == 0:
                self.current_time = self.short_break
                self.label.config(text="Short Break", fg="blue")
            else:
                self.current_time = self.work_time
                self.label.config(text="Work", fg="green")
            self.countdown(self.current_time)

    def stop_timer(self):
        if self.timer_running:
            self.timer_running = False

            if self.countdown_id:
                self.root.after_cancel(self.countdown_id)

            # No need to update the timer text since it freezes at the current time
            self.label.config(text="Stopped", fg="red")

    def reset_timer(self):
        if self.countdown_id:
            self.root.after_cancel(self.countdown_id)
        self.timer_running = False
        self.reps = 0
        self.current_time = self.work_time
        self.timer_text.set("25:00")
        self.label.config(text="Timer", fg="black")

    def countdown(self, count):
        minutes = count // 60
        seconds = count % 60
        self.timer_text.set(f"{minutes:02d}:{seconds:02d}")
        if count > 0:
            self.countdown_id = self.root.after(1000, self.countdown, count - 1)
        else:
            self.timer_running = False
            self.start_timer()
            if self.reps % 2 == 0:
                messagebox.showinfo("Break Time", "Take a short break!")
            else:
                messagebox.showinfo("Work Time", "Time to get back to work!")


class AnalogClock(tk.Canvas):
    def __init__(self, root, size=200):
        tk.Canvas.__init__(self, root, width=size, height=size, bg="white")
        self.size = size
        self.center = size // 2
        self.radius = size // 2 - 10

    def update_time(self):
        self.delete("hands")
        now = time.localtime()
        self.draw_hand(360 / 12 * (now.tm_hour % 12) + (now.tm_min / 60) * 30, self.radius * 0.5, width=6)  # Hour hand
        self.draw_hand(360 / 60 * now.tm_min, self.radius * 0.75, width=4)  # Minute hand
        self.draw_hand(360 / 60 * now.tm_sec, self.radius * 0.9, width=2, color="red")  # Second hand
        self.draw_clock_face()

    def draw_hand(self, angle, length, width=2, color="black"):
        angle_rad = math.radians(angle - 90)
        x = self.center + length * math.cos(angle_rad)
        y = self.center + length * math.sin(angle_rad)
        self.create_line(self.center, self.center, x, y, width=width, fill=color, tags="hands")

    def draw_clock_face(self):
        for i in range(12):
            angle = math.radians(360 / 12 * (i + 1) - 90)
            x = self.center + self.radius * 0.9 * math.cos(angle)
            y = self.center + self.radius * 0.9 * math.sin(angle)
            self.create_text(x, y, text=str(i + 1 if i < 11 else 12), font=("Helvetica", 14))


if __name__ == "__main__":
    root = tk.Tk()
    pomodoro_timer = PomodoroTimer(root)
    root.mainloop()
