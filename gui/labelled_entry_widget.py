import tkinter as tk
from typing import Optional

import gui


class LabelledEntryWidget(tk.Frame):
    def __init__(self, label_text: str = "", entry_width: int = 10,
                 invalid_bg: str = "#D7806D", **kwargs):
        super().__init__(**kwargs)
        self._label = tk.Label(master=self, text=label_text)
        self._entry = gui.SmartEntryWidget(master=self, width=entry_width, invalid_bg=invalid_bg)
        self._label.grid(row=0, column=0)
        self._entry.grid(row=0, column=2)

        # Forward the value changed event;
        self._entry.bind("<<Value-Changed>>", lambda _: self.event_generate("<<Value-Changed>>"))

    def get(self) -> Optional[str]:
        """Returns the text content of the view."""
        return self._entry.get()

    def clear(self) -> None:
        """Clears the textbox."""
        self._entry.clear()

    def make_invalid(self) -> None:
        """Sets the textbox to valid."""
        self._entry.make_invalid()

    def make_valid(self) -> None:
        """Sets the textbox to invalid."""
        self._entry.make_valid()
