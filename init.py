"""A nice effect player for some digital DnD 🐉🎲"""
from tkinter import *
from macro_prompt import MacroPrompt
from sound_entity import SoundEntity
from constants import (
    EFFECTS_FOLDER,
    MUSIC_FOLDER,
    COPYRIGHT_FONT,
    GLOBAL_FONT,
    HEADER_FONT,
    MAIN_WINDOW,
)
import os
import vlc

# Constant instances
media_player_effects = vlc.MediaPlayer()
player_music = vlc.Instance("--input-repeat=999999")
media_player_music = player_music.media_list_player_new()

effect_entities = []
music_entities = []


def insert_music(list_box, folder):
    """Fetches all files from a folder and inserts it sorted into a ListBox."""
    entitycollection = []
    for filename in sorted(os.listdir(folder)):
        if not filename.endswith(".gitignore"):
            new_entity = SoundEntity(filename)
            entitycollection.append(new_entity)
            list_box.insert(END, new_entity.display())

    return entitycollection


def effect_selection_changed(event = None):
    """Eventhandler for Effect change."""
    selection = lb_effects.curselection()
    media_player_effects.stop()
    if selection:
        current_effects_media = vlc.Media(
            os.path.join(EFFECTS_FOLDER, effect_entities[selection[0]].get_file())
        )
        media_player_effects.set_media(current_effects_media)
        media_player_effects.play()


def music_selection_changed(event = None):
    """Eventhandler for Music change."""
    selection = lb_music.curselection()
    media_player_music.stop()
    if selection:
        current_music_media = player_music.media_new(
            os.path.join(MUSIC_FOLDER, music_entities[selection[0]].get_file())
        )
        music_media_list = player_music.media_list_new()
        music_media_list.add_media(current_music_media)

        media_player_music.set_media_list(music_media_list)
        media_player_music.play()


def effect_macro_change(event):
    """Update macro for current effect."""
    selection = lb_effects.curselection()
    print("selection")
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
    print(event.char)
    macro_focus(event.char, effect_entities, lb_effects, effect_selection_changed)
    macro_focus(event.char, music_entities, lb_music, music_selection_changed)


if __name__ == "__main__":
    window = Tk()

    # Window settings
    window.title("EffectPlayer")
    window.geometry(MAIN_WINDOW)
    window.bind("<KeyPress>", keyboard_event)

    # Widgets
    lb_effects = Listbox(window, font=GLOBAL_FONT, exportselection=False)
    lb_music = Listbox(window, font=GLOBAL_FONT, exportselection=False)

    # Load data
    effect_entities = insert_music(lb_effects, EFFECTS_FOLDER)
    music_entities = insert_music(lb_music, MUSIC_FOLDER)

    # Ready window
    Label(window, font=HEADER_FONT, text="EffectPlayer").pack(fill="x")
    Frame(window, height=1, bg="black").pack(fill="x")
    Label(window, font=GLOBAL_FONT, text="Volume:", anchor="w").pack(fill="x")
    s_volume = Scale(
        window,
        font=GLOBAL_FONT,
        from_=0,
        to=100,
        orient=HORIZONTAL,
        command=update_volume,
    )
    s_volume.set(100)
    s_volume.pack(fill="x")
    Frame(window, height=1, bg="black").pack(fill="x")
    Label(window, font=GLOBAL_FONT, text="Effects:", anchor="w").pack(fill="x")
    lb_effects.bind("<<ListboxSelect>>", effect_selection_changed)
    lb_effects.bind("<Control-Button-1>", effect_macro_change)
    lb_effects.pack(fill="both", expand=True)
    Label(window, font=GLOBAL_FONT, text="Music:", anchor="w").pack(fill="x")
    lb_music.bind("<<ListboxSelect>>", music_selection_changed)
    lb_music.bind("<Control-Button-1>", music_macro_change)
    lb_music.pack(fill="both", expand=True)
    Button(window, font=GLOBAL_FONT, text="STOP", command=stop_everything).pack(
        fill="both", expand=True
    )
    Label(window, font=COPYRIGHT_FONT, text="Made by Vira", anchor="e").pack(fill="x")

    # Start
    window.mainloop()
