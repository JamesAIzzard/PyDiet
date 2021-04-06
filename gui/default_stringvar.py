import tkinter as tk
from typing import Optional


class DefaultStringVar(tk.StringVar):
    def __init__(self, value: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.set(value)

    def set(self, value: Optional[str]) -> None:
        if value is None or value == "":
            value = "undefined"
        super().set(value)
