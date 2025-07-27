"""A class containing interface entity properties."""


class InterfaceEntity:
    """A class containing interface entity properties"""

    def __init__(self, column: int, columnspan: int, row: int):
        self._column = column
        self._columnspan = columnspan
        self._row = row

    @property
    def column(self) -> int:
        """Int representing column position."""
        return self._column

    @property
    def row(self) -> int:
        """Int representing row position."""
        return self._row

    @property
    def columnspan(self) -> int:
        """Int representing column span."""
        return self._columnspan
