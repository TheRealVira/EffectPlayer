# pylint: disable=too-many-ancestors
"""A sound manager for effects and music.
"""
import os
import tkinter as tk
from tkinter import ttk
import pygame
from manager.config import CONFIG
from interface.macro import MacroPrompt
from entity.sound import SoundEntity
from entity.contentfolder import ContentfolderEntity
from entity.interface import InterfaceEntity
from entity.player import PlayerEntity


class SoundManager(ttk.LabelFrame):
    """UI Sound manager for effects and music."""

    def __init__(
        self,
        frame: ttk.LabelFrame,
        contentfolder_entity: ContentfolderEntity,
        interface_entity: InterfaceEntity,
        player_entity: PlayerEntity,
    ):
        """Constructs and initializes a SoundManager.

        Args:
            frame (ttk.LabelFrame): Parent Frame.
            contentfolder_entity (ContentfolderEntity): Folder containing content which
                is intended to get utelized by this SoundManager instance.
            interface_entity (InterfaceEntity): Define Interface specific information.
            player_entity (PlayerEntity): Define music player specific information.
        """
        self.contentfolder_entity = contentfolder_entity
        self.interface_entity = interface_entity
        ttk.LabelFrame.__init__(
            self, master=frame, text=self.contentfolder_entity.title
        )
        self.entities = []
        self.player_entity = player_entity

        self.grid(
            row=self.interface_entity.row,
            column=self.interface_entity.column,
            columnspan=self.interface_entity.columnspan,
            sticky="NEWS",
            padx=CONFIG.getint("default", "PAD_X"),
            pady=CONFIG.getint("default", "PAD_Y"),
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
        """Returns a constant player channel as a property.

        Returns:
            int: Defines a channel number.
        """
        return self.player_entity.channel

    def get_volume(self) -> float:
        """Returns the current volume for this SoundManager instance.

        Returns:
            float: Represents a value between 0 and 1.
        """
        return float(self.s_volume.get() / 100)

    def insert_sound(self, pre_load: bool) -> None:
        """Fetches all files from a folder and inserts it sorted into a ListBox.

        Args:
            pre_load (bool): true: Pre-Loads music; false: Skips pre-loading.
        """
        self.entities = []
        for filename in sorted(os.listdir(self.contentfolder_entity.folder)):
            if not filename.endswith(".gitignore"):
                new_entity = SoundEntity(
                    os.path.join(self.contentfolder_entity.folder, filename), pre_load
                )
                self.entities.append(new_entity)
                self.tree.insert(
                    "", tk.END, new_entity.display, text=new_entity.display
                )

    def macro_change(self, _: None) -> None:
        """Updates macro for specific content selection.

        Args:
            _ (None): Unused event parameter required by ttk.
        """
        if self.tree.focus():
            selection = self.get_entity_from_string(self.tree.focus())
            if selection:
                new_macro = MacroPrompt()
                new_macro.subscribe(selection.set_macro)
                new_macro.ask(selection.display)

    def macro_focus(self, macro: str) -> None:
        """Select and focus on content based macros.

        Args:
            macro (str): Macro key used to filter.
        """
        for entity in self.entities:
            e_macro = entity.get_macro()
            if e_macro and e_macro == macro:
                self.tree.selection_set(entity.display)
                self.tree.focus_set()
                self.tree.focus(entity.display)

    def selection_event_handler(self, _: None) -> None:
        """Gets selection from focus and starts playing it.

        Args:
            _ (None): Unused event parameter required by ttk.
        """
        if self.tree.selection():
            selection = self.get_entity_from_string(self.tree.focus())
            if selection:
                selection.play(self.player_entity.channel, self.player_entity.loops)

    def get_entity_from_string(self, entity_name: str) -> SoundEntity:
        """Tries to fetch Soundentity from content list based on the entities name.

        Args:
            entity_name (str): Entity name for SoundEntity.

        Returns:
            SoundEntity: Either reutrns the SoundEntity on success, or null otherwise.
        """
        if entity_name:
            for entity in self.entities:
                if entity.display == entity_name:
                    return entity

        return None

    def stop_everything(self) -> None:
        """Unselects everything from content lists and stops playing."""
        self.tree.selection_set("")
        pygame.mixer.Channel(self.player_entity.channel).fadeout(
            CONFIG.getint("default", "FADING")
        )

    def update_volume(self, _: None) -> None:
        """Eventhandler to detect volume changes and adapt internal volume to new value.

        Args:
            _ (None): Unused event parameter required by ttk.
        """
        pygame.mixer.Channel(self.player_entity.channel).set_volume(self.get_volume())
