import enum


class TimerStates(enum.Enum):
    IDLE = 0
    WORK = 1
    SHORT_BREAK = 2
    LONG_BREAK = 3
    PAUSED = 4
