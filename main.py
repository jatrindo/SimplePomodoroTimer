import ui
from pomodoro_timer import PomodoroTimer

# Constant Globals
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

ptimer = PomodoroTimer(WORK_MIN, SHORT_BREAK_MIN, LONG_BREAK_MIN)
ui.PomodoroInterface(ptimer)