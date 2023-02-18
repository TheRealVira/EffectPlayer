"""A prompt for keyboard macros"""
from constants import GLOBAL_FONT, PAD_X, PAD_Y
from tkinter import *


class MacroPrompt:
    """A prompt class for keyboard macros"""

    def __init__(self):
        """Initializes new prompt"""
        self.prompt = Toplevel()
        self.to_return = '""'
        self.row = -1
        self.prompt.bind("<KeyPress>", self.keyboard_event)
        self.input_display = LabelFrame(
            self.prompt, text="Input:", padx=PAD_X, pady=PAD_Y
        )
        self.macro_label = Label(self.input_display, font=GLOBAL_FONT, text="")

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

        Label(self.prompt, font=GLOBAL_FONT, text=f"Macro for: {prompt_text}").grid(
            row=self.get_row(), sticky="NEWS", padx=PAD_X, pady=PAD_Y
        )
        self.macro_label.grid(row=0, column=0, sticky="NEWS")
        Button(self.prompt, text="Accept", command=self.accept_button_event).grid(
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
        self.macro_label.config(text=f'"{event.char}"')
        self.to_return = event.char

    def accept_button_event(self):
        """Quits the prompt."""
        self.prompt.destroy()
