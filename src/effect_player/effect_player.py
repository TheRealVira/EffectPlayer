"""A nice effect player for some digital DnD 🐉🎲
"""
import contextlib

with contextlib.redirect_stdout(None):
    import pygame
import pygame.midi
from interface.main import MainWindow
from manager.midi import MidiManager
from manager.config import CONFIG

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
        clock.tick(CONFIG.getint("default", "TICKS"))
        window.update()
        midiManager.update()

    # Quit
    pygame.midi.quit()
    pygame.mixer.quit()
    pygame.quit()

    # Destroy window, if not already closed.
    if "normal" == window.state():
        window.destroy()
