#!/usr/bin/env python
import vlc, os, time
from tkinter import *

# Folder
effects_folder = "Input/Effects"
music_folder = "Input/Music"

# Constant instances
media_player_effects = vlc.MediaPlayer()
player_music = vlc.Instance("--input-repeat=999999")
media_player_music = player_music.media_list_player_new()
global_font = ('Arial', 14)

window=Tk()

# Window settings
window.title('EffectPlayer')
window.geometry("300x1000+10+20")

# Widgets
lb_effects = Listbox(window, font=global_font, exportselection = False)
lb_music = Listbox(window, font=global_font, exportselection = False)

# Effects
for filename in sorted(os.listdir(effects_folder)):
    lb_effects.insert(END, filename)

# Music
for filename in sorted(os.listdir(music_folder)):
    lb_music.insert(END, filename)
    
# Events
# Effect Event
def effectSelectionChanged(event):
    selection = lb_effects.curselection()
    media_player_effects.stop()
    if selection:
        current_effects_media = vlc.Media(os.path.join(effects_folder, event.widget.get(selection[0])))
        media_player_effects.set_media(current_effects_media)
        media_player_effects.play()

# Music Event
def musicSelectionChanged(event):
    selection = lb_music.curselection()
    media_player_music.stop()
    if selection:
        current_music_media = player_music.media_new(os.path.join(music_folder, event.widget.get(selection[0])))
        music_media_list = player_music.media_list_new()
        music_media_list.add_media(current_music_media)
        
        media_player_music.set_media_list(music_media_list)
        media_player_music.play()

# Stop all the sounds
def stopEverything():
    lb_effects.selection_clear(0, 'end')
    lb_music.selection_clear(0, 'end')
    media_player_effects.stop()
    media_player_music.stop()

# Update all volumes
def updateVolume(event):
    new_volume = s_volume.get()
    media_player_effects.audio_set_volume(new_volume)
    media_player_music.get_media_player().audio_set_volume(new_volume)

# Ready window
Label(window, font=('Arial', 20), text="EffectPlayer").pack(fill="x")
Frame(window,height=1,bg="black").pack(fill="x")
Label(window, font=global_font, text="Volume:", anchor="w").pack(fill="x")
s_volume = Scale(window, font=global_font, from_=0, to=100, orient=HORIZONTAL, command=updateVolume)
s_volume.set(100)
s_volume.pack(fill="x")
Frame(window,height=1,bg="black").pack(fill="x")
Label(window, font=global_font, text="Effects:", anchor="w").pack(fill="x")
lb_effects.bind("<<ListboxSelect>>", effectSelectionChanged)
lb_effects.pack(fill="both", expand=True)
Label(window, font=global_font, text="Music:", anchor="w").pack(fill="x")
lb_music.bind("<<ListboxSelect>>", musicSelectionChanged)
lb_music.pack(fill="both", expand=True)
Button(window, font=global_font, text="STOP", command=stopEverything).pack(fill="both", expand=True)
Label(window, font=('Arial', 8), text="Made by Vira", anchor="e").pack(fill="x")

# Start
window.mainloop()
