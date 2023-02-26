"""A class defining a sound entity"""
from pathlib import Path


class SoundEntity:
    """A class defining a sound entity"""

    def __init__(self, file: str):
        self.file = file
        self.macro = ""

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

    def set_file(self, new_file: str):
        """Sets new file path"""
        self.file = new_file

    def get_file(self) -> str:
        """Returns file path"""
        return self.file
