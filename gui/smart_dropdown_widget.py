import tkinter as tk
from tkinter import ttk
from typing import List, Optional


class SmartDropdownWidget(ttk.Combobox):
    def __init__(self, **kwargs):
        self._value = tk.StringVar()  # So we can trace changes.
        super().__init__(textvar=self._value, state="readonly", **kwargs)

        # Raise event when value changes.
        self._value.trace_add("write", callback=lambda *args: self.event_generate("<<Value-Changed>>"))

    def add_options(self, options: List[str]) -> None:
        """Adds the list of options to the dropdown box, if not already there."""
        for option in options:
            if option not in self['values']:
                self['values'] = (*self['values'], option)

    def remove_options(self, options: Optional[List[str]] = None) -> None:
        """Removes the list of options from the dropdown box, if they are there."""
        if options is None:
            self['values'] = []
        else:
            values = list(self['values'])
            for option in options:
                if option in values:
                    values.remove(option)
            self['values'] = tuple(values)

    def refresh_options(self, options: List[str]) -> None:
        """Removes all existing options and replaces them with the new list."""
        if not options == self['values']:
            self.remove_options()
            self.add_options(options)

    def set(self, value: str) -> None:
        """Sets the value of the dropdown."""
        if not value == self._value.get():
            if value not in self['values']:
                raise ValueError(f'{value} is not an option for this dropdown box.')
            self._value.set(value=value)

    def get(self) -> str:
        """Gets the current value of the dropdown."""
        return self._value.get()
