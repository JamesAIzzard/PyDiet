import tkinter as tk

import gui


class DensityEditorWidget(tk.Frame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Build the UI elements;
        self._vol_value_and_unit = gui.EntryDropdownWidget(
            master=self,
            entry_width=10,
            invalid_bg=gui.configs.invalid_bg_colour,
            dropdown_width=5
        )
        self._vol_value_and_unit.grid(row=0, column=0)
        self._label = tk.Label(master=self, text=" weighs ")
        self._label.grid(row=0, column=1)
        self._mass_value_and_unit = gui.EntryDropdownWidget(
            master=self,
            entry_width=10,
            invalid_bg=gui.configs.invalid_bg_colour,
            dropdown_width=5
        )
        self._mass_value_and_unit.grid(row=0, column=2)
