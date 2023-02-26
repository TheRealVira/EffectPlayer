"""A nice effect player for some digital DnD 🐉🎲"""
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import pygame.midi
import constants
from code.main_window import MainWindow


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    pygame.midi.init()

    default_midi_input_id = pygame.midi.get_default_input_id()
    default_midi_input = None
    if default_midi_input_id != -1:
        default_midi_input = pygame.midi.Input(default_midi_input_id)

    window = MainWindow()

    clock = pygame.time.Clock()

    while not window.is_done:
        clock.tick(constants.TICKS)
        try:
            window.update()

            # Handle MIDI
            if default_midi_input:
                if default_midi_input.poll():
                    midi_events = default_midi_input.read(10)
                    pygame_midi_events = pygame.midi.midis2events(
                        midi_events, default_midi_input.device_id
                    )
                    for midi_event in pygame_midi_events:
                        print(midi_event.dict)

        except Exception as e:
            print(f"[ERR] {e}")

    # Quit
    pygame.midi.quit()
    pygame.mixer.quit()
    pygame.quit()

    # Destroy window, if not already closed.
    if "normal" == window.state():
        window.destroy()
