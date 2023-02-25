"""A sound manager for effects and music."""
from code.sound_manager import SoundManager
import pygame
from code.constants import EFFECTS_FOLDER, FADING


class EffectManager(SoundManager):
    """An abstract sound manager and UI element."""

    def __init__(self, frame, row, column, columnspan):
        self.pygame_effect = None
        super().__init__(
            frame=frame,
            folder=EFFECTS_FOLDER,
            title="Effects:",
            row=row,
            column=column,
            columnspan=columnspan,
        )

    def load_sound(self, soundfile):
        """Loads sound during selection change. Fading is taken care of."""
        pygame.mixer.Channel(1).fadeout(FADING)
        pygame.time.wait(FADING)
        pygame.mixer.Channel(1).play(pygame.mixer.Sound(soundfile), fade_ms=FADING)

    def set_volume(self, volume):
        """Update volume event handler."""
        pygame.mixer.Channel(1).set_volume(volume)

    def stop_everything(self):
        """Stop playing sounds and unselect everything in listbox."""
        super().stop_everything()
        pygame.mixer.Channel(1).fadeout(FADING)
