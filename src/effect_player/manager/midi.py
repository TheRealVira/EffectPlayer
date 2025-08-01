"""Manages MIDI input and events."""

from collections import defaultdict
import pygame
from manager.config import CONFIG


class KeyCodeEvent:
    """A class representing keycode event."""

    def __init__(self, keycode) -> None:
        self._keycode = keycode

    @property
    def keycode(self):
        """Contains keycode."""
        return self._keycode

    @property
    def char(self):
        """Contains char of keycode."""
        return chr(self._keycode)


class MidiManager:
    """Manages MIDI input and events."""

    observers = defaultdict(list)
    _instances = []

    def __init__(self, midi_input) -> None:
        self.midi_input = midi_input
        MidiManager._instances.append(self)

    @classmethod
    def subscribe(cls, function) -> None:
        """Subscribe to MidiManager events."""
        cls.observers["Keypress"].append(function)

    @classmethod
    def unsubscribe(cls, function) -> None:
        """Remove subscription from MidiManager events."""
        if function in cls.observers["Keypress"]:
            cls.observers["Keypress"].remove(function)

    @classmethod
    def notify_keypress(cls, keycode):
        """Manually notify all observers of a keypress (for keyboard integration)."""
        for function in cls.observers["Keypress"]:
            function(KeyCodeEvent(keycode))

    @classmethod
    def update_all(cls):
        """Update all instances of MidiManager."""
        for instance in cls._instances:
            instance.update()

    def update(self) -> None:
        """Update Midi Manager."""
        if self.midi_input:
            if self.midi_input.poll():
                midi_events = self.midi_input.read(
                    CONFIG.getint("default", "MIDI_NOTES")
                )
                pygame_midi_events = list(
                    filter(
                        lambda e: e.dict["status"]
                        == CONFIG.getint("default", "MIDI_ON_NOTE_STATUS"),
                        pygame.midi.midis2events(
                            midi_events, self.midi_input.device_id
                        ),
                    )
                )

                # Trigger event for subscribers:
                for midi_event in pygame_midi_events:
                    for function in self.observers["Keypress"]:
                        function(KeyCodeEvent(midi_event.dict["data1"]))
