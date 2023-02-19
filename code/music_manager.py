from code.sound_manager import SoundManager
from tkinter import *
import vlc
import time
import os

class MusicManager(SoundManager):
    def __init__(self, frame, folder, row, column, columnspan):
        super().__init__(frame = frame, folder = folder, row =row, column = column, columnspan=columnspan, title="Music:")
        self.player_music = vlc.Instance("--input-repeat=999999")
        self.media_player = self.player_music.media_list_player_new()

    def change_media(self):
        """Music change."""
        selection = self.list_box.curselection()
        while self.media_player.get_media_player().audio_get_volume() > 0:
            self.media_player.get_media_player().audio_set_volume(
                self.media_player.get_media_player().audio_get_volume() - 1
            )
            time.sleep(0.005)
        self.media_player.stop()
        current_music_media = self.player_music.media_new(
            os.path.join(self.folder, self.entities[selection[0]].get_file())
        )
        music_media_list = self.player_music.media_list_new()
        music_media_list.add_media(current_music_media)

        self.media_player.set_media_list(music_media_list)
        self.media_player.play()
        while self.media_player.get_media_player().audio_get_volume() < self.s_volume.get():
            self.media_player.get_media_player().audio_set_volume(
                self.media_player.get_media_player().audio_get_volume() + 1
            )
            time.sleep(0.005)

        self.media_player.get_media_player().audio_set_volume(self.s_volume.get())
