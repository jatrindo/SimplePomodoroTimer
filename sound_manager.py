import os
from playsound import playsound


class SoundManager:

    def __init__(self, sounds_dir: str) -> None:
        self.sounds_dir = os.path.abspath(sounds_dir)

    def play_enter_short_break_sound(self):
        sound = os.path.join(self.sounds_dir, "bell_ding.wav")
        playsound(sound, False)

    def play_enter_long_break_sound(self):
        sound = os.path.join(self.sounds_dir, "phone_ding.wav")
        playsound(sound, False)
