"""A class defining a sound entity"""
from pathlib import Path


class SoundEntity:
    """A class defining a sound entity"""

    def __init__(self, file):
        self.file = file
        self.macro = ""

    def display(self):
        """Returns filename without extension."""
        return Path(self.file).stem

    def set_macro(self, macro):
        """Sets new macro"""
        self.macro = macro

    def get_macro(self):
        """Returns macro"""
        return self.macro

    def set_file(self, new_file):
        """Sets new file path"""
        self.file = new_file

    def get_file(self):
        """Returns file path"""
        return self.file
