import tkinter as tk

import gui


class PieceMassEditorWidget(tk.Frame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Build the UI elements;
        self._num_pieces = gui.SmartEntryWidget(
            master=self,
            width=10,
            invalid_bg=gui.configs.invalid_bg_colour
        )
        self._num_pieces.grid(row=0, column=0)
        self._label = tk.Label(master=self, text=" piece(s) weighs ")
        self._label.grid(row=0, column=1)
        self._pieces_mass = gui.EntryDropdownWidget(
            master=self,
            entry_width=10,
            invalid_bg=gui.configs.invalid_bg_colour,
            dropdown_width=5
        )
        self._pieces_mass.grid(row=0, column=2)
