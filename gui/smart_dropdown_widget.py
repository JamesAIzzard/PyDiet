import tkinter as tk
from tkinter import ttk
from typing import List, Optional

import model


def configure_qty_units(dropdown: 'SmartDropdownWidget', subject: 'model.quantity.HasBulk') -> None:
    """Configures the dropdown widget to match the subject's configured units."""
    # Save the old value;
    prev_value = dropdown.get()
    # Clear it all out;
    dropdown.remove_options()
    # Repopulate with correct options;
    dropdown.add_options(model.quantity.get_recognised_mass_units())
    if subject.density_is_defined:
        dropdown.add_options(model.quantity.get_recognised_vol_units())
    if subject.piece_mass_defined:
        dropdown.add_options(model.quantity.get_recognised_pc_units())
    # Reinstate the old value if it is still available;
    if prev_value in dropdown['values']:
        dropdown.set(prev_value)


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
        self.remove_options()
        self.add_options(options)

    def set(self, value: str) -> None:
        """Sets the value of the dropdown."""
        if value not in self['values']:
            raise ValueError(f'{value} is not an option for this dropdown box.')
        self._value.set(value=value)

    def get(self) -> str:
        """Gets the current value of the dropdown."""
        return self._value.get()
