"""Constants.. just constants."""
import os

# Font
HEADER_FONT = ("Arial", 20)
FOOTER_FONT = ("Arial", 7)

# Folder
INPUT_FOLDER = "Input"
EFFECTS_FOLDER = "Effects"
MUSIC_FOLDER = "Music"
EFFECTS_FOLDER_ABS = os.path.abspath(os.path.join(INPUT_FOLDER, EFFECTS_FOLDER))
MUSIC_FOLDER_ABS = os.path.abspath(os.path.join(INPUT_FOLDER, MUSIC_FOLDER))

# Geometry
PAD_X = 10
PAD_Y = 5

# MIDI
MIDI_NOTES = 10
MIDI_ON_NOTE_STATUS = 153  # magic numberz

# Other
FADING = 250
THEME = "yaru"
TICKS = 100
PRE_LOAD_SOUNDS = True
