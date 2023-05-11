"""A prompt for keyboard macros"""
import tkinter as tk
from tkinter import ttk
from code.midi_manager import MidiManager
import config.constants


class MacroPrompt(tk.Toplevel):
    """A prompt class for keyboard macros"""

    def __init__(self):
        """Initializes new prompt"""
        tk.Toplevel.__init__(self)
        self.to_return = '""'
        self.row = -1
        self.observers = []
        self.bind("<KeyPress>", self.keyboard_event)
        MidiManager.subscribe(self.keyboard_event)
        self.input_display = ttk.LabelFrame(self, text="Input:")
        self.macro_label = ttk.Label(self.input_display, text="")
        self.protocol("WM_DELETE_WINDOW", self.quit)

    def subscribe(self, function) -> None:
        """Subscribe to when the user accepts a macro."""
        self.observers.append(function)

    def get_row(self) -> int:
        """Returns incremental row."""
        self.row += 1
        return self.row

    def ask(self, prompt_text: str):
        """Opens a new prompt and returns a key, if not cancelled."""
        self.title("Bind macro")
        self.resizable(False, False)
        self.columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.input_display.columnconfigure(0, weight=1)
        self.input_display.grid_rowconfigure(0, weight=1)
        self.input_display.grid(
            column=self.get_row(),
            sticky="NEWS",
            padx=config.constants.PAD_X,
            pady=config.constants.PAD_Y,
        )

        ttk.Label(self, text=f"Macro for: {prompt_text}").grid(
            row=self.get_row(),
            sticky="NEWS",
            padx=config.constants.PAD_X,
            pady=config.constants.PAD_Y,
        )
        self.macro_label.grid(row=0, column=0, sticky="NEWS")
        ttk.Button(self, text="Accept", command=self.accept_button_event).grid(
            row=self.get_row(),
            column=0,
            sticky="NEWS",
            padx=config.constants.PAD_X,
            pady=config.constants.PAD_Y,
        )

        self.lift()
        self.focus_force()
        self.grab_set()

    def keyboard_event(self, event) -> None:
        """Eventhandler for keyboard macros."""
        self.macro_label.config(text=f'keycode: {event.keycode}: "{event.char}"')
        self.to_return = event.keycode

    def accept_button_event(self) -> None:
        """Quits the prompt."""
        for function in self.observers:
            function(self.to_return)
        self.quit()

    def quit(self) -> None:
        """Make sure to clean up."""
        MidiManager.unsubscribe(self.keyboard_event)
        self.destroy()
