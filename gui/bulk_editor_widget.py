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


class BulkEditorWidget(tk.LabelFrame):
    def __init__(self, **kwargs):
        super().__init__(text="Bulk Properties", **kwargs)
        self._ref_qty_and_unit_entry = gui.LabelledEntryDropdownWidget(
            master=self,
            label_text="Reference Quantity: ",
            entry_width=10,
            dropdown_width=5,
            invalid_bg=gui.configs.invalid_bg_colour,
        )
        self._density_entry = DensityEditorWidget(master=self)
        self._pc_mass_entry = PieceMassEditorWidget(master=self)
        self._ref_qty_and_unit_entry.grid(row=0, column=0, sticky="w")
        self._density_entry.grid(row=1, column=0, sticky="w")
        self._pc_mass_entry.grid(row=2, column=0, sticky="w")


class HasBulkEditorWidget(gui.HasSubject):
    def __init__(self, bulk_editor_widget: 'gui.BulkEditorWidget', **kwargs):
        super().__init__(**kwargs)
        self._bulk_editor_widget = bulk_editor_widget

    def _on_ref_qty_value_change(self, _) -> None:
        """Handles changes to the reference quantity value."""


    def _on_ref_qty_unit_change(self, _) -> None:
        """Handles changes to the reference quantity unit."""

    def _on_density_mass_value_change(self, _) -> None:
        """Handles changes to the density mass value."""

    def _on_density_mass_unit_change(self, _) -> None:
        """Handles changes to the density mass unit."""

    def _on_density_vol_value_change(self, _) -> None:
        """Handles changes to the density volume value."""

    def _on_density_vol_unit_change(self, _) -> None:
        """Handles changes to the density volume unit."""

    def _on_piece_value_change(self, _) -> None:
        """Handles changes to the peice value."""

    def _on_piece_mass_value_change(self, _) -> None:
        """Handles changes to the piece mass value."""

    def _on_piece_mass_unit_change(self, _) -> None:
        """Handles changes to the piece mass unit."""
