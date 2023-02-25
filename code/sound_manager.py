"""A sound manager for effects and music."""
import os
from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import ttk
from code.sound_entity import SoundEntity
from code.macro_prompt import MacroPrompt
from code.constants import (
    PAD_X,
    PAD_Y,
)


class SoundManager(ABC):
    """An abstract sound manager and UI element."""

    def __init__(self, frame, folder, title, row, column, columnspan):
        self.entities = []
        self.folder = folder

        self.frame = ttk.LabelFrame(frame, text=title)
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
        self.s_volume = ttk.Scale(
            self.frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            command=self.update_volume,
        )
        self.s_volume.set(100)
        self.s_volume.grid(row=0, column=0, sticky="NEWS")

        # Sound selection listbox
        self.tree = ttk.Treeview(self.frame, selectmode="browse", show="tree")
        self.tree.bind("<<TreeviewSelect>>", self.selection_event_handler)
        self.tree.bind("<Control-Button-1>", self.macro_change)
        self.tree.grid(column=0, row=1, sticky="NEWS")

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(
            self.frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(column=1, row=1, sticky="NS")

    def get_volume(self):
        """Returns volume as int."""
        return int(self.s_volume.get())

    def insert_sound(self):
        """Fetches all files from a folder and inserts it sorted into a ListBox."""
        self.entities = []
        for filename in sorted(os.listdir(self.folder)):
            if not filename.endswith(".gitignore"):
                new_entity = SoundEntity(filename)
                self.entities.append(new_entity)
                self.tree.insert(
                    "", tk.END, new_entity.display(), text=new_entity.display()
                )

    def macro_change(self, event):
        """Update macro for current effect."""
        if self.tree.focus():
            selection = self.get_entity_from_string(self.tree.focus())
            if selection:
                new_macro = MacroPrompt().ask(selection.display())
                if new_macro:
                    selection.set_macro(new_macro)

    def macro_focus(self, macro):
        """Select entities based on macro"""
        for entity in self.entities:
            e_macro = entity.get_macro()
            if e_macro and e_macro == macro:
                self.tree.selection_set(entity.display())
                self.tree.focus_set()
                self.tree.focus(entity.display())

    def selection_event_handler(self, event=None):
        """Eventhandler for Music change."""
        if self.tree.selection():
            selection = self.get_entity_from_string(self.tree.focus())
            if selection:
                self.load_sound(os.path.join(self.folder, selection.get_file()))

    def get_entity_from_string(self, entity_name):
        """If entity exists, function returns name of entity. Else it returns None."""
        if entity_name:
            for entity in self.entities:
                if entity.display() == entity_name:
                    return entity

        return None

    def update_volume(self, event):
        """Event Handler for volume change."""
        self.set_volume(self.get_volume())

    @abstractmethod
    def load_sound(self, soundfile):
        """Loads sound during selection change. Fading is taken care of."""

    @abstractmethod
    def set_volume(self, volume):
        """Sets volume."""

    @abstractmethod
    def stop_everything(self):
        """Stop playing sounds and unselect everything in listbox."""
        self.tree.selection_set("")
