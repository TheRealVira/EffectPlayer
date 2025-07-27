"""A nice effect player for some digital DnD 🐉🎲"""

import contextlib

with contextlib.redirect_stdout(None):
    import pygame
import pygame.midi

from interface.main import MainWindow
from manager.midi import MidiManager
from manager.config import CONFIG

midi_event_handlers = []


def get_default_midi_input():
    """Return a pygame.midi.Input object if a device is available, else None."""
    try:
        default_id = pygame.midi.get_default_input_id()
        if default_id != -1:
            print(f"Using default MIDI input device ID: {default_id}")
            return pygame.midi.Input(default_id)
    except pygame.midi.MidiException:
        pass
    return None


if __name__ == "__main__":
    pygame.init()  # pylint: disable=no-member
    pygame.mixer.init()
    pygame.midi.init()
    pygame.mixer.set_num_channels(16)

    DEFAULT_MIDI_INPUT = get_default_midi_input()
    midiManager = MidiManager(midi_input=DEFAULT_MIDI_INPUT)

    window = MainWindow()

    clock = pygame.time.Clock()

    while not window.is_done:
        clock.tick(CONFIG.getint("default", "TICKS"))
        window.update()
        midiManager.update()  # Handles both MIDI and keyboard events

    # Quit
    pygame.midi.quit()
    pygame.mixer.quit()
    pygame.quit()  # pylint: disable=no-member

    # Destroy window, if not already closed.
    if "normal" == window.state():
        window.destroy()
