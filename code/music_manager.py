"""A sound manager for effects and music."""
from code.sound_manager import SoundManager
import pygame
from code.constants import MUSIC_FOLDER, FADING


class MusicManager(SoundManager):
    """An abstract sound manager and UI element."""

    def __init__(self, frame, row, column, columnspan):
        super().__init__(
            frame=frame,
            folder=MUSIC_FOLDER,
            title="Music:",
            row=row,
            column=column,
            columnspan=columnspan,
        )

    def load_sound(self, soundfile):
        """Loads sound during selection change. Fading is taken care of."""
        pygame.mixer.Channel(0).fadeout(FADING)
        pygame.time.wait(FADING)
        pygame.mixer.Channel(0).play(
            pygame.mixer.Sound(soundfile), loops=-1, fade_ms=FADING
        )

    def set_volume(self, volume):
        """Update volume event handler."""
        pygame.mixer.Channel(0).set_volume(volume)

    def stop_everything(self):
        """Stop playing sounds and unselect everything in listbox."""
        super().stop_everything()
        pygame.mixer.Channel(0).fadeout(FADING)
