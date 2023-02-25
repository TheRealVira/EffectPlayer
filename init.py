"""A nice effect player for some digital DnD 🐉🎲"""
import tkinter as tk
import pygame
from tkinter import ttk
from ttkthemes import ThemedTk
from code.effect_manager import EffectManager
from code.sound_manager import SoundManager
from code.music_manager import MusicManager
from code.constants import (
    HEADER_FONT,
    PAD_X,
    PAD_Y,
    THEME,
)

ROW = -1
sound_managers = []


def get_row():
    """Returns incremental row."""
    global ROW
    return (ROW := ROW + 1)


def keyboard_event(event):
    """Macro keyboard event handler."""
    for sound_manager in sound_managers:
        sound_manager.macro_focus(event.keycode)


def stop_everything():
    """Stop button event handler."""
    for sound_manager in sound_managers:
        sound_manager.stop_everything()


if __name__ == "__main__":
    # Window settings
    window = ThemedTk(theme="yaru")
    window.title("EffectPlayer")
    window.columnconfigure(0, weight=1)
    window.resizable(False, False)
    window.grid_rowconfigure(0, weight=1)
    window.bind("<KeyPress>", keyboard_event)

    pygame.init()
    pygame.mixer.init()

    # Style
    style = ttk.Style(window)
    style.theme_use(THEME)

    ttk.Label(window, font=HEADER_FONT, text="EffectPlayer").grid(
        row=get_row(), column=0, sticky="NEWS"
    )

    effect_manager = EffectManager(
        frame=window,
        row=get_row(),
        column=0,
        columnspan=3,
    )
    effect_manager.insert_sound()
    sound_managers.append(effect_manager)

    music_manager = MusicManager(frame=window, row=get_row(), column=0, columnspan=3)
    music_manager.insert_sound()
    sound_managers.append(music_manager)

    ttk.Button(window, text="STOP", command=stop_everything).grid(
        row=get_row(), columnspan=2, sticky="EWS", padx=PAD_X, pady=PAD_Y
    )
    ttk.Label(window, text="Made by Vira").grid(
        row=ROW, column=2, sticky="EWS", padx=PAD_X, pady=PAD_Y
    )

    # Start
    window.mainloop()
