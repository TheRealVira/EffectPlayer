"""A nice effect player for some digital DnD 🐉🎲"""
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import pygame.midi
import constants
from code.main_window import MainWindow
from code.midi_manager import MidiManager

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
        clock.tick(constants.TICKS)
        window.update()
        midiManager.update()

    # Quit
    pygame.midi.quit()
    pygame.mixer.quit()
    pygame.quit()

    # Destroy window, if not already closed.
    if "normal" == window.state():
        window.destroy()
