"""A class containing player entity properties.
"""


class PlayerEntity:
    """A class containing player entity properties"""

    def __init__(self, channel: int, loops: int = 0):
        self._channel = channel
        self._loops = loops

    @property
    def channel(self) -> int:
        """Int defining player channel."""
        return self._channel

    @property
    def loops(self) -> int:
        """Int defining how many times a player should loop. 0=no loop, -1=infinite loop"""
        return self._loops
