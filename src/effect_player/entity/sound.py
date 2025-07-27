"""A class defining a sound entity."""

from pathlib import Path
import pygame
from effect_player.manager.config import CONFIG


class SoundEntity:
    """A class defining a sound entity"""

    def __init__(self, file: str, preload: bool):
        self.file = file
        self.macro = ""
        self.sound = pygame.mixer.Sound(self.file) if preload else None

    @property
    def display(self) -> str:
        """Returns filename without extension."""
        return Path(self.file).stem

    def set_macro(self, macro: str):
        """Sets new macro"""
        self.macro = macro

    def get_macro(self) -> str:
        """Returns macro"""
        return self.macro

    def get_sound(self) -> pygame.mixer.Sound:
        """Returns pygame Sound entity"""
        if not self.sound:
            self.sound = pygame.mixer.Sound(self.file)
        return self.sound

    def play(self, channel: int, loops: int):
        """Plays da tunes. Fading is taken care of."""
        pygame.mixer.Channel(channel).fadeout(CONFIG.getint("default", "FADING"))
        pygame.time.wait(CONFIG.getint("default", "FADING") + 100)
        pygame.mixer.Channel(channel).play(
            self.get_sound(), loops=loops, fade_ms=CONFIG.getint("default", "FADING")
        )
