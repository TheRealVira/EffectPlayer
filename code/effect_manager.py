from code.sound_manager import SoundManager
from tkinter import *
import vlc
import time
import os

class EffectManager(SoundManager):
    def __init__(self, frame, folder, row, column, columnspan):
        super().__init__(frame = frame, folder = folder, row =row, column = column, columnspan=columnspan, title="Effect:")

    def change_media(self):
        """Effect change."""
        selection = self.list_box.curselection()
        while self.media_player.audio_get_volume() > 0:
            self.media_player.audio_set_volume(
                self.media_player.audio_get_volume() - 1
            )
            time.sleep(0.005)
        self.media_player.stop()
        current_effects_media = vlc.Media(
            os.path.join(self.folder, self.entities[selection[0]].get_file())
        )
        self.media_player.set_media(current_effects_media)
        self.media_player.play()
        while self.media_player.audio_get_volume() < self.s_volume.get():
            self.media_player.audio_set_volume(
                self.media_player.audio_get_volume() + 1
            )
            time.sleep(0.005)

        self.media_player.audio_set_volume(self.s_volume.get())
