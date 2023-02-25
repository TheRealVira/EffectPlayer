"""A prompt for keyboard macros"""
from code.constants import PAD_X, PAD_Y
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk


class MacroPrompt:
    """A prompt class for keyboard macros"""

    def __init__(self):
        """Initializes new prompt"""
        self.prompt = tk.Toplevel()
        self.to_return = '""'
        self.row = -1
        self.prompt.bind("<KeyPress>", self.keyboard_event)
        self.input_display = ttk.LabelFrame(self.prompt, text="Input:")
        self.macro_label = ttk.Label(self.input_display, text="")

    def get_row(self):
        """Returns incremental row."""
        self.row += 1
        return self.row

    def ask(self, prompt_text):
        """Opens a new prompt and returns a key, if not cancelled."""
        self.prompt.title("Bind macro")
        self.prompt.resizable(False, False)
        self.prompt.columnconfigure(0, weight=1)
        self.prompt.grid_rowconfigure(0, weight=1)
        self.input_display.columnconfigure(0, weight=1)
        self.input_display.grid_rowconfigure(0, weight=1)
        self.input_display.grid(
            column=self.get_row(), sticky="NEWS", padx=PAD_X, pady=PAD_Y
        )

        ttk.Label(self.prompt, text=f"Macro for: {prompt_text}").grid(
            row=self.get_row(), sticky="NEWS", padx=PAD_X, pady=PAD_Y
        )
        self.macro_label.grid(row=0, column=0, sticky="NEWS")
        ttk.Button(self.prompt, text="Accept", command=self.accept_button_event).grid(
            row=self.get_row(),
            column=0,
            sticky="NEWS",
            padx=PAD_X,
            pady=PAD_Y,
        )

        self.prompt.lift()
        self.prompt.focus_force()
        self.prompt.grab_set()
        self.prompt.wait_window()

        return self.to_return

    def keyboard_event(self, event):
        """Eventhandler for keyboard macros."""
        self.macro_label.config(text=f'keycode: {event.keycode}: "{event.char}"')
        self.to_return = event.keycode

    def accept_button_event(self):
        """Quits the prompt."""
        self.prompt.destroy()
