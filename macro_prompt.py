"""A prompt for keyboard macros"""
from constants import GLOBAL_FONT, MACRO_PROMPT
from tkinter import *
from tkinter.ttk import *


class MacroPrompt:
    """A prompt class for keyboard macros"""

    def __init__(self):
        """Initializes new prompt"""
        self.prompt = Toplevel()
        self.to_return = ""
        self.macro_label = Label(self.prompt, font=GLOBAL_FONT, text="")

    def ask(self, prompt_text):
        """Opens a new prompt and returns a key, if not cancelled."""
        self.prompt.bind("<KeyPress>", self.keyboard_event)
        self.prompt.geometry(MACRO_PROMPT)
        self.prompt.title("Bind macro")
        Label(self.prompt, font=GLOBAL_FONT, text=prompt_text).pack()
        self.macro_label.pack()
        self.prompt.lift()
        self.prompt.focus_force()
        self.prompt.grab_set()

        self.prompt.wait_window()
        print("finished waiting...")
        return self.to_return

    def keyboard_event(self, event):
        """Eventhandler for keyboard macros."""
        self.macro_label.config(text=event.char)
        self.to_return = event.char
