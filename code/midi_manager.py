"""Manages MIDI input and events."""
from collections import defaultdict
import pygame
import config.constants


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

    def __init__(self, midi_input) -> None:
        self.midi_input = midi_input

    @classmethod
    def subscribe(cls, function) -> None:
        """Subscribe to MidiManager events."""
        cls.observers["Keypress"].append(function)

    @classmethod
    def unsubscribe(cls, function) -> None:
        """Remove subscription from MidiManager events."""
        cls.observers["Keypress"].remove(function)

    def update(self) -> None:
        """Update Midi Manager."""
        if self.midi_input:
            if self.midi_input.poll():
                midi_events = self.midi_input.read(config.constants.MIDI_NOTES)
                pygame_midi_events = list(
                    filter(
                        lambda e: e.dict["status"]
                        == config.constants.MIDI_ON_NOTE_STATUS,
                        pygame.midi.midis2events(
                            midi_events, self.midi_input.device_id
                        ),
                    )
                )

                # Trigger event for subscribers:
                for midi_event in pygame_midi_events:
                    for function in self.observers["Keypress"]:
                        function(KeyCodeEvent(midi_event.dict["data1"]))
