"""A nice effect player for some digital DnD 🐉🎲"""
import os
import contextlib

with contextlib.redirect_stdout(None):
    import pygame
from code.main_window import MainWindow
from code.midi_manager import MidiManager
import pygame.midi
import config.constants

midi_event_handlers = []

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    pygame.midi.init()

    default_midi_input_id = pygame.midi.get_default_input_id()
    DEFAULT_MIDI_INPUT = None
    if default_midi_input_id != -1:
        DEFAULT_MIDI_INPUT = pygame.midi.Input(default_midi_input_id)

    midiManager = MidiManager(midi_input=DEFAULT_MIDI_INPUT)

    window = MainWindow()

    clock = pygame.time.Clock()

    while not window.is_done:
        clock.tick(config.constants.TICKS)
        window.update()
        midiManager.update()

    # Quit
    pygame.midi.quit()
    pygame.mixer.quit()
    pygame.quit()

    # Destroy window, if not already closed.
    if "normal" == window.state():
        window.destroy()
