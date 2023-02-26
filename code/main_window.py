"""A nice effect player for some digital DnD 🐉🎲"""
import webbrowser
from tkinter import ttk
from ttkthemes import ThemedTk
from code.sound_manager import SoundManager
from code.midi_manager import MidiManager
import constants


class MainWindow(ThemedTk):
    """Main Window containing all widgets."""

    def __init__(self) -> None:
        ThemedTk.__init__(self, theme=constants.THEME)
        self.row = -1
        self._done = False
        self.sound_managers = []
        self.title("EffectPlayer")
        self.columnconfigure(0, weight=1)
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=1)
        self.bind("<KeyPress>", self.keyboard_event)
        self.protocol("WM_DELETE_WINDOW", self.quit)

        MidiManager.subscribe(self.keyboard_event)

        # Style
        style = ttk.Style(self)
        style.theme_use(constants.THEME)

        ttk.Label(self, font=constants.HEADER_FONT, text="EffectPlayer").grid(
            row=self.get_row(), columnspan=3, sticky=""
        )

        effect_manager = SoundManager(
            frame=self,
            row=self.get_row(),
            column=0,
            columnspan=3,
            title="Effects:",
            channel=0,
            folder=constants.EFFECTS_FOLDER,
        )
        effect_manager.insert_sound()
        self.sound_managers.append(effect_manager)

        music_manager = SoundManager(
            frame=self,
            row=self.get_row(),
            column=0,
            columnspan=3,
            title="Music:",
            channel=1,
            loops=-1,
            folder=constants.MUSIC_FOLDER,
        )
        music_manager.insert_sound()
        self.sound_managers.append(music_manager)

        ttk.Button(self, text="STOP", command=self.stop_everything).grid(
            row=self.get_row(),
            columnspan=2,
            sticky="EWS",
            padx=constants.PAD_X,
            pady=constants.PAD_Y,
        )
        footer = ttk.Label(
            self,
            font=constants.FOOTER_FONT,
            text="Made by Vira",
            foreground="blue",
            cursor="hand2",
        )
        footer.configure(underline=True)
        footer.bind(
            "<Button-1>",
            lambda e: webbrowser.open("https://github.com/TheRealVira/EffectPlayer"),
        )
        footer.grid(
            row=self.row,
            column=2,
            sticky="EWS",
            padx=constants.PAD_X,
            pady=constants.PAD_Y,
        )

    @property
    def is_done(self) -> bool:
        """Returns false if window is still running; False if all is done."""
        return self._done

    def quit(self) -> None:
        """Sets done to True."""
        self._done = True

    def keyboard_event(self, event) -> None:
        """Macro keyboard event handler."""
        for sound_manager in self.sound_managers:
            sound_manager.macro_focus(event.keycode)

    def stop_everything(self) -> None:
        """Stop button event handler."""
        for sound_manager in self.sound_managers:
            sound_manager.stop_everything()

    def get_row(self) -> int:
        """Returns incremental row."""
        self.row += 1
        return self.row
