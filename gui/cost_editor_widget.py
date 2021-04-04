import tkinter as tk
from tkinter import ttk
from typing import List

import gui


class CostEditorWidget(tk.Frame):
    """View to display/manipulate the cost of a substance per quantity."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create the components;
        self._cost_label = tk.Label(master=self, text="Cost: £")
        self._cost_label.grid(row=0, column=0)
        self._cost_entry = gui.SmartEntryWidget(master=self, width=10, invalid_bg=gui.configs.invalid_bg_colour)
        self._cost_entry.grid(row=0, column=1)
        self._per_label = tk.Label(master=self, text=" per ")
        self._per_label.grid(row=0, column=2)
        self._qty_entry = gui.SmartEntryWidget(master=self, width=5, invalid_bg=gui.configs.invalid_bg_colour)
        self._qty_entry.grid(row=0, column=3)
        self._qty_units_dropdown = ttk.Combobox(master=self, width=5, value=['g', 'kg'])
        self._qty_units_dropdown.grid(row=0, column=4)

        # Wire up events;
        self._cost_entry.bind("<<Value-Changed>>", lambda _: self.event_generate("<<Cost-Changed>>"))
        self._qty_entry.bind("<<Value-Changed>>", lambda _: self.event_generate("<<Qty-Changed>>"))

    @property
    def cost_value(self) -> float:
        """Returns the contents of the cost value entry box."""
        if self._cost_entry.get() == "":
            return 0
        else:
            return float(self._cost_entry.get())

    @property
    def qty_value(self) -> float:
        """Returns the contents of the qty value entry box."""
        if self._qty_entry.get() == "":
            return 0
        else:
            return float(self._qty_entry.get())

    def add_qty_units(self, qty_units: List[str]) -> None:
        """Adds quantity units to the units dropdown box."""

    def remove_qty_units(self, qty_units: List[str]) -> None:
        """Removes quantity units from the units dropdown box."""

    @property
    def cost_in_valid_state(self) -> bool:
        """Returns True/False to indicate if the cost entry is in invalid state."""
        return not self._cost_entry.in_invalid_state

    def make_cost_invalid(self) -> None:
        """Sets the cost entry box to its invalid state."""
        self._cost_entry.make_invalid()

    def make_cost_valid(self) -> None:
        """Sets the cost entry box to its valid state."""
        self._cost_entry.make_valid()

    @property
    def qty_in_valid_state(self) -> bool:
        """Returns True/False to indicate if the qty entry is in invalid state."""
        return not self._qty_entry.in_invalid_state

    def make_qty_invalid(self) -> None:
        """Sets the qty entry box to its invalid state."""
        self._qty_entry.make_invalid()

    def make_qty_valid(self) -> None:
        """Sets the qty entry box to its valid state."""
        self._qty_entry.make_valid()
