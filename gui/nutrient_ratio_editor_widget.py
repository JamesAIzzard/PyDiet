import tkinter as tk
from typing import Optional, Union

import gui


class NutrientRatioEditorWdiget(tk.Frame):
    """Widget to manipulate the quantity of a nutrient per quantity of subject."""

    def __init__(self, nutrient_name: str, **kwargs):
        """
        Notes:
            We provide the opportunity to pass the subject name as a StringVar to
            provide the opportunity to syncronise the name with the display in
            other places in the UI.
        """
        super().__init__(**kwargs)

        # Create the nutrient name;
        self._nutrient_name_label = tk.Label(master=self, text=f"{nutrient_name} :")
        self._nutrient_name_label.grid(row=0, column=0)

        # Create the nutrient mass and qty widget;
        self._nutrient_mass_and_unit = gui.EntryDropdownWidget(
            master=self,
            entry_width=10,
            invalid_bg=gui.configs.invalid_bg_colour,
            dropdown_width=5
        )
        self._nutrient_mass_and_unit.grid(row=0, column=1)

        # Create the 'in' label;
        self._in = tk.Label(master=self, text=" in ")
        self._in.grid(row=0, column=2)

        # Create the subject mass and qty widget;
        self._subject_qty_and_unit = gui.EntryDropdownWidget(
            master=self,
            entry_width=10,
            invalid_bg=gui.configs.invalid_bg_colour,
            dropdown_width=5,
        )
        self._subject_qty_and_unit.grid(row=0, column=3)

    @property
    def subject_qty_value(self) -> Optional[float]:
        """Returns the value of the subject quantity."""

    @property
    def subject_qty_unit(self) -> str:
        """Returns the unit of the subject quantity."""

    @property
    def nutrient_mass_value(self) -> Optional[float]:
        """Returns the nutrient mass value."""

    @property
    def nutrient_mass_unit(self) -> str:
        """Returns the nutrient mass unit."""
