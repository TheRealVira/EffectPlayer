"""A sound manager for effects and music."""
import os
import tkinter as tk
from tkinter import ttk
import pygame
from code.sound_entity import SoundEntity
from code.macro_prompt import MacroPrompt
import constants


class SoundManager(ttk.LabelFrame):
    """An abstract sound manager and UI element."""

    def __init__(
        self,
        frame,
        folder: str,
        title: str,
        row: int,
        column: int,
        columnspan: int,
        channel: int,
        loops: int = 0,
    ):
        ttk.LabelFrame.__init__(self, master=frame, text=title)
        self.entities = []
        self.folder = folder
        self._channel = channel
        self.loops = loops

        self.grid(
            row=row,
            column=column,
            columnspan=columnspan,
            sticky="NEWS",
            padx=constants.PAD_X,
            pady=constants.PAD_Y,
        )
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Volume
        self.s_volume = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            command=self.update_volume,
        )
        self.s_volume.set(100)
        self.s_volume.grid(row=0, column=0, sticky="NEWS")

        # Sound selection listbox
        self.tree = ttk.Treeview(self, selectmode="browse", show="tree")
        self.tree.bind("<<TreeviewSelect>>", self.selection_event_handler)
        self.tree.bind("<Control-Button-1>", self.macro_change)
        self.tree.grid(column=0, row=1, sticky="NEWS")

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(column=1, row=1, sticky="NS")

    @property
    def channel(self) -> int:
        """PyGame mixer channel"""
        return self._channel

    def get_volume(self) -> float:
        """Returns volume as int."""
        return float(self.s_volume.get() / 100)

    def insert_sound(self) -> None:
        """Fetches all files from a folder and inserts it sorted into a ListBox."""
        self.entities = []
        for filename in sorted(os.listdir(self.folder)):
            if not filename.endswith(".gitignore"):
                new_entity = SoundEntity(filename)
                self.entities.append(new_entity)
                self.tree.insert(
                    "", tk.END, new_entity.display, text=new_entity.display
                )

    def macro_change(self, event) -> None:
        """Update macro for current effect."""
        if self.tree.focus():
            selection = self.get_entity_from_string(self.tree.focus())
            if selection:
                new_macro = MacroPrompt()
                new_macro.subscribe(selection.set_macro)
                new_macro.ask(selection.display)

    def macro_focus(self, macro: str) -> None:
        """Select entities based on macro"""
        for entity in self.entities:
            e_macro = entity.get_macro()
            if e_macro and e_macro == macro:
                self.tree.selection_set(entity.display)
                self.tree.focus_set()
                self.tree.focus(entity.display)

    def selection_event_handler(self, event=None) -> None:
        """Eventhandler for Music change."""
        if self.tree.selection():
            selection = self.get_entity_from_string(self.tree.focus())
            if selection:
                self.load_sound(os.path.join(self.folder, selection.get_file()))

    def get_entity_from_string(self, entity_name: str) -> SoundEntity:
        """If entity exists, function returns name of entity. Else it returns None."""
        if entity_name:
            for entity in self.entities:
                if entity.display == entity_name:
                    return entity

        return None

    def stop_everything(self) -> None:
        """Stop playing sounds and unselect everything in listbox."""
        self.tree.selection_set("")
        pygame.mixer.Channel(self.channel).fadeout(constants.FADING)

    def update_volume(self, event) -> None:
        """Event Handler for volume change."""
        pygame.mixer.Channel(self.channel).set_volume(self.get_volume())

    def load_sound(self, soundfile: str) -> None:
        """Loads sound during selection change. Fading is taken care of."""
        pygame.mixer.Channel(self.channel).fadeout(constants.FADING)
        pygame.time.wait(constants.FADING)
        pygame.mixer.Channel(self.channel).play(
            pygame.mixer.Sound(soundfile), loops=self.loops, fade_ms=constants.FADING
        )
