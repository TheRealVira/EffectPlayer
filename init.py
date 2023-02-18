"""A nice effect player for some digital DnD 🐉🎲"""
from tkinter import *
import threading
import time
import os
import vlc
from macro_prompt import MacroPrompt
from sound_entity import SoundEntity
from constants import (
    EFFECTS_FOLDER,
    MUSIC_FOLDER,
    COPYRIGHT_FONT,
    GLOBAL_FONT,
    HEADER_FONT,
    PAD_X,
    PAD_Y,
)

# Constant instances
vlc.Instance()
media_player_effects = vlc.MediaPlayer()
player_music = vlc.Instance("--input-repeat=999999")
media_player_music = player_music.media_list_player_new()

ROW = -1

effect_entities = []
music_entities = []


def get_row():
    """Returns incremental row."""
    global ROW
    return (ROW := ROW + 1)


def insert_music(list_box, folder):
    """Fetches all files from a folder and inserts it sorted into a ListBox."""
    entitycollection = []
    for filename in sorted(os.listdir(folder)):
        if not filename.endswith(".gitignore"):
            new_entity = SoundEntity(filename)
            entitycollection.append(new_entity)
            list_box.insert(END, new_entity.display())

    return entitycollection


def effect_selection_changed(event=None):
    """Eventhandler for Effect change."""
    selection = lb_effects.curselection()
    if selection and effect_entities[selection[0]].display() is not selection:
        thread = threading.Thread(target=change_effect)
        thread.start()


def change_effect():
    """Effect change."""
    selection = lb_effects.curselection()
    while media_player_effects.audio_get_volume() > 0:
        media_player_effects.audio_set_volume(
            media_player_effects.audio_get_volume() - 1
        )
        time.sleep(0.005)
    media_player_effects.stop()
    current_effects_media = vlc.Media(
        os.path.join(EFFECTS_FOLDER, effect_entities[selection[0]].get_file())
    )
    media_player_effects.set_media(current_effects_media)
    media_player_effects.play()
    while media_player_effects.audio_get_volume() < s_volume.get():
        media_player_effects.audio_set_volume(
            media_player_effects.audio_get_volume() + 1
        )
        time.sleep(0.005)

    media_player_effects.audio_set_volume(s_volume.get())


def music_selection_changed(event=None):
    """Eventhandler for Music change."""
    selection = lb_music.curselection()
    if selection and music_entities[selection[0]].display() is not selection:
        thread = threading.Thread(target=change_music)
        thread.start()


def change_music():
    """Music change."""
    selection = lb_music.curselection()
    while media_player_music.get_media_player().audio_get_volume() > 0:
        media_player_music.get_media_player().audio_set_volume(
            media_player_music.get_media_player().audio_get_volume() - 1
        )
        time.sleep(0.005)
    media_player_music.stop()
    current_music_media = player_music.media_new(
        os.path.join(MUSIC_FOLDER, music_entities[selection[0]].get_file())
    )
    music_media_list = player_music.media_list_new()
    music_media_list.add_media(current_music_media)

    media_player_music.set_media_list(music_media_list)
    media_player_music.play()
    while media_player_music.get_media_player().audio_get_volume() < s_volume.get():
        media_player_music.get_media_player().audio_set_volume(
            media_player_music.get_media_player().audio_get_volume() + 1
        )
        time.sleep(0.005)

    media_player_music.get_media_player().audio_set_volume(s_volume.get())


def effect_macro_change(event):
    """Update macro for current effect."""
    selection = lb_effects.curselection()
    if selection:
        new_macro = MacroPrompt().ask(event.widget.get(selection[0]))
        if new_macro:
            effect_entities[selection[0]].set_macro(new_macro)


def music_macro_change(event):
    """Update macro for current music."""
    selection = lb_music.curselection()
    if selection:
        new_macro = MacroPrompt().ask(event.widget.get(selection[0]))
        if new_macro:
            music_entities[selection[0]].set_macro(new_macro)


def stop_everything():
    """Eventhandler to stop music and effects."""
    lb_effects.selection_clear(0, "end")
    lb_music.selection_clear(0, "end")
    media_player_effects.stop()
    media_player_music.stop()


def update_volume():
    """Eventhandler to change volume."""
    new_volume = s_volume.get()
    media_player_effects.audio_set_volume(new_volume)
    media_player_music.get_media_player().audio_set_volume(new_volume)


def macro_focus(macro, entities, listbox, func):
    """Select entities based on macro"""
    for i in range(len(entities)):
        if entities[i].get_macro() and entities[i].get_macro() is macro:
            listbox.selection_clear(0, END)
            listbox.select_set(i)
            listbox.activate(i)
            func()


def keyboard_event(event):
    """Eventhandler for keyboard macros."""
    macro_focus(event.char, effect_entities, lb_effects, effect_selection_changed)
    macro_focus(event.char, music_entities, lb_music, music_selection_changed)


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

    # Frames
    effect_frame = LabelFrame(window, text="Effects:")
    music_frame = LabelFrame(window, text="Music:")
    volume_frame = LabelFrame(window, text="Volume:")

    # Frame grid config
    volume_frame.grid(row=get_row(), columnspan=3, sticky="NEW", padx=PAD_X, pady=PAD_Y)
    volume_frame.grid_rowconfigure(0, weight=1)
    volume_frame.grid_columnconfigure(0, weight=1)
    effect_frame.grid(
        row=get_row(), columnspan=3, sticky="NEWS", padx=PAD_X, pady=PAD_Y
    )
    effect_frame.grid_rowconfigure(0, weight=1)
    effect_frame.grid_columnconfigure(0, weight=1)
    music_frame.grid(row=get_row(), columnspan=3, sticky="NEWS", padx=PAD_X, pady=PAD_Y)
    music_frame.grid_rowconfigure(0, weight=1)
    music_frame.grid_columnconfigure(0, weight=1)

    # Widgets
    s_volume = Scale(
        volume_frame,
        font=GLOBAL_FONT,
        from_=0,
        to=100,
        orient=HORIZONTAL,
        command=update_volume,
    )
    s_volume.set(100)
    s_volume.grid(row=0, column=0, sticky="NEWS")

    lb_effects = Listbox(effect_frame, font=GLOBAL_FONT, exportselection=False)
    lb_effects.bind("<<ListboxSelect>>", effect_selection_changed)
    lb_effects.bind("<Control-Button-1>", effect_macro_change)
    lb_effects.grid(column=0, row=0, sticky="NEWS")

    lb_music = Listbox(music_frame, font=GLOBAL_FONT, exportselection=False)
    lb_music.bind("<<ListboxSelect>>", music_selection_changed)
    lb_music.bind("<Control-Button-1>", music_macro_change)
    lb_music.grid(column=0, row=0, sticky="NEWS")

    # Load data
    effect_entities = insert_music(lb_effects, EFFECTS_FOLDER)
    music_entities = insert_music(lb_music, MUSIC_FOLDER)

    Button(window, font=GLOBAL_FONT, text="STOP", command=stop_everything).grid(
        row=get_row(), columnspan=2, sticky="EWS", padx=PAD_X, pady=PAD_Y
    )
    Label(window, font=COPYRIGHT_FONT, text="Made by Vira").grid(
        row=ROW, column=2, sticky="EWS", padx=PAD_X, pady=PAD_Y
    )

    # Start
    window.mainloop()
