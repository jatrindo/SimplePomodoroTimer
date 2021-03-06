import calendar
import datetime as dt
import json
import tkinter as tk

from pomodoro_timer import PomodoroTimer
from sound_manager import SoundManager
from timer_states import TimerStates

# Appearance
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"


class PomodoroInterface(object):

    def __init__(self, ptimer: PomodoroTimer, sound_manager: SoundManager):
        self.ptimer = ptimer
        self.sound_manager = sound_manager
        self.countdown_timer = None
        self.start_time = ""

        # Window
        self.window = tk.Tk()
        self.window.title("Pomodoro")
        self.window.config(padx=100, pady=50, bg=YELLOW)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Labels
        self.title_label = tk.Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 28, "bold"))
        self.title_label.grid(row=0, column=1)

        self.checkmarks_label = tk.Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 30, "bold"))
        self.checkmarks_label.grid(row=5, column=1)

        self.total_time_spent_label = tk.Label(
            text="Total Time Spent: 00h 00m 00s",
            fg=GREEN,
            bg=YELLOW,
            font=(FONT_NAME, 20, "bold")
        )
        self.total_time_spent_label.grid(row=6, column=0, columnspan=3)

        # Entries
        self.current_activity_entry = tk.Entry(width=27)
        self.current_activity_entry.insert(tk.END, string="Activity Here!")
        self.current_activity_entry.grid(row=3, column=1)

        # Text Boxes
        self.activity_detail_text = tk.Text(height=5, width=35)
        self.activity_detail_text.insert(tk.END, "Activity Detail")
        self.activity_detail_text.grid(row=4, column=1, pady=1)

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
        # Don't save if we were idle and the user pressed the reset button
        if self.ptimer.state != TimerStates.IDLE:
            self.save_session()

        self.ptimer.reset()
        self.update_time_displays()
        self.start_time = ""

        self.window.title("Pomodoro")
        self.title_label.config(text="Timer", fg=GREEN)
        self.checkmarks_label.config(text="")
        self.start_pause_button.config(text="Start")

    def start_pause_timer(self):
        button_state = self.start_pause_button.cget("text")
        if button_state == "Start":
            # Update the text
            self.start_time = self.__get_current_time()
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
        previous_state = self.ptimer.state
        self.ptimer.count_down()
        current_state = self.ptimer.state

        self.update_time_displays()

        # Detect if there was a change of state
        if previous_state != current_state:
            if current_state == TimerStates.WORK:
                self.sound_manager.play_enter_work_session_sound()
                self.title_label.config(text="Work", fg=GREEN)

            if current_state == TimerStates.SHORT_BREAK:
                self.sound_manager.play_enter_short_break_sound()
                self.checkmarks_label.config(text="???" * self.ptimer.num_sessions)
                self.title_label.config(text="Break", fg=PINK)

            if current_state == TimerStates.LONG_BREAK:
                self.sound_manager.play_enter_long_break_sound()
                self.checkmarks_label.config(text="???" * self.ptimer.num_sessions)
                self.title_label.config(text="Break", fg=RED)

            if current_state == TimerStates.PAUSED:
                self.title_label.config(text="Paused", fg=YELLOW)

        # Count down again after a second
        self.countdown_timer = self.window.after(1000, self.count_down)

    def save_session(self):
        session_file = "session_log.json"

        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
        except FileNotFoundError:
            session_data = {
                "sessions": []
            }

        current_session = {
            "date": self.__get_current_date(),
            "day_of_week": self.__get_current_day_of_week(),
            "activity_title": self.__get_activity_title(),
            "activity_detail": self.__get_activity_detail(),
            "start_time": self.__get_start_time(),
            "end_time": self.__get_end_time(),
            "num_completed_sessions": self.__get_num_completed_sessions(),
            "total_time_seconds": self.__get_total_seconds(),
            "total_time_hms": self.__get_total_time_hms()
        }

        session_data.get("sessions").append(current_session)

        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=4)

    def on_closing(self):
        # Save the session if it's in-progress
        if self.ptimer.state != TimerStates.IDLE:
            self.save_session()

        self.window.destroy()

    @staticmethod
    def __get_current_time():
        return str(dt.datetime.now())

    @staticmethod
    def __get_current_date():
        return str(dt.datetime.now().date())

    @staticmethod
    def __get_current_day_of_week():
        return calendar.day_name[dt.datetime.now().weekday()]

    def __get_activity_title(self):
        return self.current_activity_entry.get()

    def __get_activity_detail(self):
        return self.activity_detail_text.get("1.0", tk.END).strip()

    def __get_start_time(self):
        return self.start_time

    def __get_end_time(self):
        return self.__get_current_time()

    def __get_num_completed_sessions(self):
        return self.ptimer.num_sessions

    def __get_total_seconds(self):
        return self.ptimer.total_ticks

    def __get_total_time_hms(self):
        return PomodoroTimer.ticks_to_str(self.ptimer.total_ticks, 'hms')
