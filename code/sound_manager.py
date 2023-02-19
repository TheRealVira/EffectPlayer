"""A sound manager for effects and music."""
import os
import threading
import time
import vlc
from tkinter import *
from code.sound_entity import SoundEntity
from code.macro_prompt import MacroPrompt
from code.constants import (
    GLOBAL_FONT,
    PAD_X,
    PAD_Y,
    FADING_SLEEP_TIME,
)


class SoundManager:
    """A class wrapping vlc media player."""

    def __init__(self, frame, folder, title, row, column, columnspan, vlc_params=""):
        self.entities = []
        self.folder = folder
        self.player_music = vlc.Instance(vlc_params)
        self.media_player = self.player_music.media_list_player_new()

        self.frame = LabelFrame(frame, text=title)
        self.frame.grid(
            row=row,
            column=column,
            columnspan=columnspan,
            sticky="NEWS",
            padx=PAD_X,
            pady=PAD_Y,
        )
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # Volume
        self.s_volume = Scale(
            self.frame,
            font=GLOBAL_FONT,
            from_=0,
            to=100,
            orient=HORIZONTAL,
            command=self.update_volume,
        )
        self.s_volume.set(100)
        self.s_volume.grid(row=0, column=0, sticky="NEWS")

        # Sound selection listbox
        self.list_box = Listbox(self.frame, font=GLOBAL_FONT, exportselection=False)
        self.list_box.bind("<<ListboxSelect>>", self.selection_event_handler)
        self.list_box.bind("<Control-Button-1>", self.macro_change)
        self.list_box.grid(column=0, row=1, sticky="NEWS")

    def insert_sound(self):
        """Fetches all files from a folder and inserts it sorted into a ListBox."""
        self.entities = []
        for filename in sorted(os.listdir(self.folder)):
            if not filename.endswith(".gitignore"):
                new_entity = SoundEntity(filename)
                self.entities.append(new_entity)
                self.list_box.insert(END, new_entity.display())

    def macro_change(self, event):
        """Update macro for current effect."""
        selection = self.list_box.curselection()
        if selection:
            new_macro = MacroPrompt().ask(event.widget.get(selection[0]))
            if new_macro:
                self.entities[selection[0]].set_macro(new_macro)

    def macro_focus(self, macro):
        """Select entities based on macro"""
        for i in range(len(self.entities)):
            if self.entities[i].get_macro() and self.entities[i].get_macro() is macro:
                self.list_box.selection_clear(0, END)
                self.list_box.select_set(i)
                self.list_box.activate(i)
                self.selection_event_handler()

    def update_volume(self, event):
        """Update volume event handler."""
        self.media_player.get_media_player().audio_set_volume(self.s_volume.get())

    def selection_event_handler(self, event=None):
        """Eventhandler for Music change."""
        selection = self.list_box.curselection()
        if selection and self.entities[selection[0]].display() is not selection:
            thread = threading.Thread(target=self.change_media)
            thread.start()

    def stop_everything(self):
        """Stop playing sounds and unselect everything in listbox."""
        self.list_box.selection_clear(0, "end")
        self.media_player.stop()

    def change_media(self):
        """Music change."""
        selection = self.list_box.curselection()
        while self.media_player.get_media_player().audio_get_volume() > 0:
            self.media_player.get_media_player().audio_set_volume(
                self.media_player.get_media_player().audio_get_volume() - 1
            )
            time.sleep(FADING_SLEEP_TIME)
        self.media_player.stop()
        current_music_media = self.player_music.media_new(
            os.path.join(self.folder, self.entities[selection[0]].get_file())
        )
        music_media_list = self.player_music.media_list_new()
        music_media_list.add_media(current_music_media)

        self.media_player.set_media_list(music_media_list)
        self.media_player.play()
        while (
            self.media_player.get_media_player().audio_get_volume()
            < self.s_volume.get()
        ):
            self.media_player.get_media_player().audio_set_volume(
                self.media_player.get_media_player().audio_get_volume() + 1
            )
            time.sleep(FADING_SLEEP_TIME)

        self.media_player.get_media_player().audio_set_volume(self.s_volume.get())
