import tkinter as tk
from typing import Optional

import gui
import model


class BulkEditorWidget(tk.Frame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._ref_qty_and_unit_entry = gui.LabelledEntryDropdownWidget(
            master=self,
            label_text="Reference Quantity: ",
            entry_width=10,
            dropdown_width=5,
            invalid_bg=gui.configs.invalid_bg_colour,
        )
        self._density_entry = gui.DensityEditorWidget(master=self)
        self._pc_mass_entry = gui.PieceMassEditorWidget(master=self)
        self._ref_qty_and_unit_entry.grid(row=0, column=0, sticky="w")
        self._density_entry.grid(row=1, column=0, sticky="w")
        self._pc_mass_entry.grid(row=2, column=0, sticky="w")


class BulkEditorController:
    def __init__(self, app: 'gui.App', view: 'BulkEditorWidget'):
        self._app = app
        self._view = view
        self._subject: Optional['model.quantity.HasSettableBulk'] = None

    @property
    def subject(self) -> Optional['model.quantity.HasSettableBulk']:
        return self._subject

    @subject.setter
    def subject(self, subject:Optional['model.quantity.HasSettableBulk']) -> None:
        self._subject = subject
