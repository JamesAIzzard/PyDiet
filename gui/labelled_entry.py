import tkinter as tk
from typing import Optional

import gui


class View(tk.Frame):
    def __init__(self, label_text: str = "", entry_width: int = 10, **kwargs):
        super().__init__(**kwargs)
        self._label = tk.Label(master=self, text=label_text)
        self._entry = tk.Entry(self, width=entry_width)
        self._label.grid(row=0, column=0)
        self._entry.grid(row=0, column=2)

    def get(self) -> Optional[str]:
        """Returns the text content of the view."""
        content = self._entry.get()
        if not content.replace(" ", "") == "":
            return None
        else:
            return content

    def clear(self) -> None:
        """Clears the textbox."""
        self._entry.delete("0", tk.END)


class Controller(gui.ViewController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
