"""A nice effect player for some digital DnD 🐉🎲"""
from tkinter import *
from code.sound_manager import SoundManager
from code.constants import (
    EFFECTS_FOLDER,
    MUSIC_FOLDER,
    COPYRIGHT_FONT,
    GLOBAL_FONT,
    HEADER_FONT,
    PAD_X,
    PAD_Y,
)

ROW = -1
sound_managers = []

def get_row():
    """Returns incremental row."""
    global ROW
    return (ROW := ROW + 1)

def keyboard_event(event):
    for sound_manager in sound_managers:
        sound_manager.macro_focus(event.char)

def stop_everything():
    for sound_manager in sound_managers:
        sound_manager.stop_everything()

if __name__ == "__main__":
    window = Tk()

    # Window settings
    window.title("EffectPlayer")
    window.columnconfigure(0, weight=1)
    window.grid_rowconfigure(0, weight=1)
    window.bind("<KeyPress>", keyboard_event)

    Label(window, font=HEADER_FONT, text="EffectPlayer").grid(
        row=get_row(), column=0, sticky="NEWS"
    )

    effect_manager = SoundManager(frame=window, folder= EFFECTS_FOLDER,row=get_row(), column=0, columnspan=3, title="Effects:")
    effect_manager.insert_sound()
    sound_managers.append(effect_manager)

    music_manager = SoundManager(frame=window, folder= MUSIC_FOLDER,row=get_row(), column=0, columnspan=3, title="Music:", vlc_params="--input-repeat=999999")
    music_manager.insert_sound()
    sound_managers.append(music_manager)


    Button(window, font=GLOBAL_FONT, text="STOP", command=stop_everything).grid(
        row=get_row(), columnspan=2, sticky="EWS", padx=PAD_X, pady=PAD_Y
    )
    Label(window, font=COPYRIGHT_FONT, text="Made by Vira").grid(
        row=ROW, column=2, sticky="EWS", padx=PAD_X, pady=PAD_Y
    )

    # Start
    window.mainloop()
