import tkinter as tk
from pomodoro_timer import PomodoroTimer
from timer_states import TimerStates

# Appearance
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"


class PomodoroInterface(object):

    def __init__(self, ptimer):
        self.ptimer = ptimer
        self.countdown_timer = None

        self.window = tk.Tk()
        self.window.title("Pomodoro")
        self.window.config(padx=100, pady=50, bg=YELLOW)

        # Labels
        self.title_label = tk.Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 28, "bold"))
        self.title_label.grid(row=0, column=1)

        self.checkmarks_label = tk.Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 30, "bold"))
        self.checkmarks_label.grid(row=4, column=1)

        self.total_time_spent_label = tk.Label(
            text="Total Time Spent: 00h 00m 00s",
            fg=GREEN,
            bg=YELLOW,
            font=(FONT_NAME, 20, "bold")
        )
        self.total_time_spent_label.grid(row=5, column=0, columnspan=3)

        # Entries
        self.current_activity_entry = tk.Entry(width=27)
        self.current_activity_entry.insert(tk.END, string="Activity Here!")
        self.current_activity_entry.grid(row=3, column=1)

        # Tomato Image with Timer
        self.canvas = tk.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
        self.tomato_img = tk.PhotoImage(file="tomato.png")
        self.canvas.create_image(100, 112, image=self.tomato_img)
        self.timer_text = self.canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 28, "bold"))
        self.canvas.grid(row=1, column=1)

        # Buttons
        self.start_pause_button = tk.Button(text="Start", command=self.start_pause_timer, highlightthickness=0)
        self.start_pause_button.grid(row=2, column=0)
        self.reset_button = tk.Button(text="Reset", command=self.reset_timer, highlightthickness=0)
        self.reset_button.grid(row=2, column=2)

        self.window.mainloop()

    def update_time_displays(self):
        tts = PomodoroTimer.ticks_to_str(self.ptimer.total_ticks, 'hms')
        self.total_time_spent_label.config(text=f"Total Time Spent: {tts}")

        ttext = PomodoroTimer.ticks_to_str(self.ptimer.timer_ticks, 'digital')
        self.canvas.itemconfig(self.timer_text, text=f"{ttext}")
        self.window.title(f"{self.title_label.cget('text')}: {ttext}")

    def cancel_timers(self):
        if self.countdown_timer:
            self.window.after_cancel(self.countdown_timer)

    def reset_timer(self):
        self.cancel_timers()

        self.ptimer.reset()
        self.update_time_displays()

        self.window.title("Pomodoro")
        self.title_label.config(text="Timer", fg=GREEN)
        self.checkmarks_label.config(text="")
        self.start_pause_button.config(text="Start")

    def start_pause_timer(self):
        button_state = self.start_pause_button.cget("text")
        if button_state == "Start":
            # Update the text
            self.start_pause_button.config(text="Pause")
            # Prep the timer and count it down
            self.ptimer.start()
            self.count_down()
        elif button_state == "Pause":
            self.start_pause_button.config(text="Resume")
            self.ptimer.pause()
            self.cancel_timers()
        elif button_state == "Resume":
            self.start_pause_button.config(text="Pause")
            self.ptimer.resume()
            self.count_down()

    def count_down(self):
        # Next tick
        self.ptimer.count_down()

        self.update_time_displays()

        if self.ptimer.state == TimerStates.WORK:
            self.title_label.config(text="Work", fg=GREEN)

        if self.ptimer.state == TimerStates.SHORT_BREAK:
            self.checkmarks_label.config(text="✓" * self.ptimer.num_sessions)
            self.title_label.config(text="Break", fg=PINK)

        if self.ptimer.state == TimerStates.LONG_BREAK:
            self.checkmarks_label.config(text="✓" * self.ptimer.num_sessions)
            self.title_label.config(text="Break", fg=RED)

        if self.ptimer.state == TimerStates.PAUSED:
            self.title_label.config(text="Paused", fg=YELLOW)

        # Count down again after a second
        self.countdown_timer = self.window.after(1000, self.count_down)