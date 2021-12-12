from timer_states import TimerStates


class PomodoroTimer(object):

    def __init__(self, work_min, short_break_min, long_break_min):
        self.work_ticks = work_min * 60
        self.sb_ticks = short_break_min * 60
        self.lb_ticks = long_break_min * 60

        self.state = TimerStates.IDLE
        self.timer_ticks = self.work_ticks
        self.total_ticks = 0
        self.num_sessions = 0
        self.resume_state = TimerStates.WORK

    def reset(self):
        self.timer_ticks = 0
        self.total_ticks = 0
        self.num_sessions = 0
        self.resume_state = None
        self.state = TimerStates.IDLE

    def start(self):
        self.state = TimerStates.WORK
        self.timer_ticks = self.work_ticks
        self.total_ticks = 0
        self.num_sessions = 0
        self.resume_state = TimerStates.WORK

    def count_down(self):
        # Do different things in response to the countdown depending on the
        # current state

        if self.state == TimerStates.IDLE:
            return
        if self.state == TimerStates.PAUSED:
            return

        if self.state == TimerStates.WORK:
            self.timer_ticks -= 1
            self.total_ticks += 1

            if self.timer_ticks <= 0:
                self.num_sessions += 1

                if self.num_sessions % 4 == 0:
                    self.state = TimerStates.LONG_BREAK
                    self.timer_ticks = self.lb_ticks
                else:
                    self.state = TimerStates.SHORT_BREAK
                    self.timer_ticks = self.sb_ticks
            return

        if self.state == TimerStates.SHORT_BREAK:
            self.timer_ticks -= 1
            self.total_ticks += 1

            if self.timer_ticks <= 0:
                self.state = TimerStates.WORK
                self.timer_ticks = self.work_ticks
            return

        if self.state == TimerStates.LONG_BREAK:
            self.timer_ticks -= 1
            self.total_ticks += 1

            if self.timer_ticks <= 0:
                self.state = TimerStates.WORK
                self.timer_ticks = self.work_ticks
            return

        raise ValueError(f"Unexpected Timer state value: {self.state}")

    @classmethod
    def ticks_to_str(cls, ticks, fmt='digital'):
        h = ticks // 3600
        m = (ticks // 60) % 60
        s = ticks % 60

        if fmt == 'hms':
            return f"{h:02d}h {m:02d}m {s:02d}s"

        if fmt == 'digital':
            return f"{m:02d}:{s:02d}"

        return f"{m:02d}:{s:02d}"
