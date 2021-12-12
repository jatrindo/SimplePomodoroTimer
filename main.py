import tkinter as tk
from pomodoro_timer import PomodoroTimer
from timer_states import TimerStates


# ---------------------------- CONSTANTS ------------------------------- #
# Appearance
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

# Constant Globals
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

# Timers
countdown_timer = None

# Pomodoro Timer
pt = PomodoroTimer(WORK_MIN, SHORT_BREAK_MIN, LONG_BREAK_MIN)


def update_time_displays():
    tts = PomodoroTimer.ticks_to_str(pt.total_ticks, 'hms')
    total_time_spent_label.config(text=f"Total Time Spent: {tts}")

    ttext = PomodoroTimer.ticks_to_str(pt.timer_ticks, 'digital')
    canvas.itemconfig(timer_text, text=f"{ttext}")
    window.title(f"{title_label.cget('text')}: {ttext}")


def cancel_timers():
    if countdown_timer:
        window.after_cancel(countdown_timer)


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    cancel_timers()

    pt.reset()
    update_time_displays()

    window.title("Pomodoro")
    title_label.config(text="Timer", fg=GREEN)
    checkmarks_label.config(text="")


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    # Prep the timer
    pt.start()
    # Count it down
    count_down()


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down():
    global countdown_timer

    # Next tick
    pt.count_down()

    update_time_displays()

    if pt.state == TimerStates.WORK:
        title_label.config(text="Work", fg=GREEN)

    if pt.state == TimerStates.SHORT_BREAK:
        checkmarks_label.config(text="✓" * pt.num_sessions)
        title_label.config(text="Break", fg=PINK)

    if pt.state == TimerStates.LONG_BREAK:
        checkmarks_label.config(text="✓" * pt.num_sessions)
        title_label.config(text="Break", fg=RED)

    if pt.state == TimerStates.PAUSED:
        title_label.config(text="Paused", fg=YELLOW)

    # Count down again after a second
    countdown_timer = window.after(1000, count_down)


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

# Labels
title_label = tk.Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 28, "bold"))
title_label.grid(row=0, column=1)

checkmarks_label = tk.Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, 30, "bold"))
checkmarks_label.grid(row=3, column=1)

total_time_spent_label = tk.Label(text="Total Time Spent: 00h 00m 00s",
                                  fg=GREEN, bg=YELLOW, font=(FONT_NAME, 20, "bold"))
total_time_spent_label.grid(row=4, column=0, columnspan=3)

# Tomato Image with Timer
canvas = tk.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = tk.PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 28, "bold"))
canvas.grid(row=1, column=1)

# Buttons
start_button = tk.Button(text="Start", command=start_timer, highlightthickness=0)
start_button.grid(row=2, column=0)
reset_button = tk.Button(text="Reset", command=reset_timer, highlightthickness=0)
reset_button.grid(row=2, column=2)

window.mainloop()
