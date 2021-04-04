import tkinter as tk
from tkinter import ttk
from typing import List

import gui


class SmartDropdownWidget(ttk.Combobox):
    def __init__(self, dropdown_width: int = None, values: List[str] = None, **kwargs):
        if values is None:
            values = []
        if dropdown_width is None:
            dropdown_width = 5
        super().__init__(values=values, width=dropdown_width, **kwargs)

    def add_options(self, options: List[str]) -> None:
        """Adds the list of options to the dropdown box, if not already there."""
        for option in options:
            if option not in self['values']:
                self['values'] = (*self['values'], option)

    def remove_options(self, options: List[str]) -> None:
        """Removes the list of options from the dropdown box, if they are there."""
        values = list(self['values'])
        for option in options:
            if option in values:
                values.remove(option)
        self['values'] = tuple(values)


class LabelledDropdownWidget(tk.Frame):
    def __init__(self, label_text: str = "", dropdown_width: int = None, values: List[str] = None, **kwargs):
        super().__init__(**kwargs)
        self._label = tk.Label(master=self, text=label_text)
        self._dropdown = SmartDropdownWidget(master=self, dropdown_width=dropdown_width, values=values)
        self._label.grid(row=0, column=0)
        self._dropdown.grid(row=0, column=1)


class EntryDropdownWidget(tk.Frame):
    def __init__(self, entry_width: int = 10, invalid_bg: str = "#D7806D",
                 values: List[str] = None, dropdown_width: int = None, **kwargs):
        super().__init__(**kwargs)
        self._entry = gui.SmartEntryWidget(master=self, width=entry_width, invalid_bg=invalid_bg)
        self._dropdown = SmartDropdownWidget(master=self, values=values, dropdown_width=dropdown_width)
        self._entry.grid(row=0, column=0)
        self._dropdown.grid(row=0, column=1)


class LabelledEntryDropdownWidget(tk.Frame):
    def __init__(self, label_text: str = "", entry_width: int = 10, invalid_bg: str = "#D7806D",
                 values: List[str] = None, dropdown_width: int=None, **kwargs):
        super().__init__(**kwargs)
        self._label = tk.Label(master=self, text=label_text)
        self._entry_dropdown = EntryDropdownWidget(master=self, entry_width=entry_width, invalid_bg=invalid_bg,
                                                   values=values, dropdown_width=dropdown_width)
        self._label.grid(row=0, column=0)
        self._entry_dropdown.grid(row=0, column=1)
