import tkinter as tk
from tkinter import ttk
from typing import List

import gui


class SmartDropdownWidget(ttk.Combobox):
    def __init__(self, dropdown_width: int = None, values: List[str] = None, **kwargs):
        self._value = tk.StringVar()  # So we can trace changes.
        if values is None:
            values = []
        if dropdown_width is None:
            dropdown_width = 5
        super().__init__(values=values, width=dropdown_width, textvar=self._value, state="readonly", **kwargs)

        # Raise event when value changes.
        self._value.trace_add("write", callback=lambda *args: self.event_generate("<<Value-Changed>>"))

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

    def set(self, value: str) -> None:
        """Sets the value of the dropdown."""
        if value not in self['values']:
            raise ValueError(f'{value} is not an option for this dropdown box.')
        self._value.set(value=value)

    def get(self) -> str:
        """Gets the current value of the dropdown."""
        return self._value.get()


class LabelledDropdownWidget(tk.Frame):
    def __init__(self, label_text: str = "", dropdown_width: int = None, values: List[str] = None, **kwargs):
        super().__init__(**kwargs)
        self._label = tk.Label(master=self, text=label_text)
        self._dropdown = SmartDropdownWidget(master=self, dropdown_width=dropdown_width, values=values)
        self._label.grid(row=0, column=0)
        self._dropdown.grid(row=0, column=1)

        # Bind events to value changes;
        self._dropdown.bind("<<Value-Changed>>", lambda _: self.event_generate("<<Value-Changed>>"))

    def set(self, value: str) -> None:
        """Sets the value of the dropdown box."""
        self._dropdown.set(value)

    def get(self) -> str:
        """Gets the value of the dropdown box."""
        self._dropdown.get()


class EntryDropdownWidget(tk.Frame):
    def __init__(self, entry_width: int = 10, invalid_bg: str = "#D7806D",
                 values: List[str] = None, dropdown_width: int = None, **kwargs):
        super().__init__(**kwargs)
        self._entry = gui.SmartEntryWidget(master=self, width=entry_width, invalid_bg=invalid_bg)
        self._dropdown = SmartDropdownWidget(master=self, values=values, dropdown_width=dropdown_width)
        self._entry.grid(row=0, column=0)
        self._dropdown.grid(row=0, column=1)

        # Bind events to dropdown and entry changes;
        self._entry.bind("<<Value-Changed>>", lambda _: self.event_generate("<<Entry-Value-Changed>>"))
        self._dropdown.bind("<<Value-Changed>>", lambda _: self.event_generate("<<Dropdown-Value-Changed>>"))


class LabelledEntryDropdownWidget(tk.Frame):
    def __init__(self, label_text: str = "", entry_width: int = 10, invalid_bg: str = "#D7806D",
                 values: List[str] = None, dropdown_width: int = None, **kwargs):
        super().__init__(**kwargs)
        self._label = tk.Label(master=self, text=label_text)
        self._entry_dropdown = EntryDropdownWidget(master=self, entry_width=entry_width, invalid_bg=invalid_bg,
                                                   values=values, dropdown_width=dropdown_width)
        self._label.grid(row=0, column=0)
        self._entry_dropdown.grid(row=0, column=1)

        # Bind events to dropdown and entry changes;
        self._entry_dropdown.bind("<<Entry-Value-Changed>>", lambda _: self.event_generate("<<Entry-Value-Changed>>"))
        self._entry_dropdown.bind(
            "<<Dropdown-Value-Changed>>",
            lambda _: self.event_generate("<<Dropdown-Value-Changed>>")
        )

        # todo
        # This re-binding events is a code smell - I should be doing this by inheritence, not composition
        # I think, this would remove the need to listen for and re-raise events.
