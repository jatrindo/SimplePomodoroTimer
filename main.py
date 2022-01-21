import os
import ui
from pomodoro_timer import PomodoroTimer
from sound_manager import SoundManager

# Constant Globals
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

sounds_dir = os.path.abspath("sounds")

sound_manager = SoundManager(sounds_dir)
ptimer = PomodoroTimer(WORK_MIN, SHORT_BREAK_MIN, LONG_BREAK_MIN)
ui.PomodoroInterface(ptimer, sound_manager)
