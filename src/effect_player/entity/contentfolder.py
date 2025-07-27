"""A class defining a contentfolder."""


class ContentfolderEntity:
    """A class defining a contentfolder"""

    def __init__(self, title: str, folder: str):
        self._title = title
        self._folder = folder

    @property
    def title(self) -> str:
        """String representing title of contentfolder."""
        return self._title

    @property
    def folder(self) -> str:
        """String containing a folder path."""
        return self._folder
