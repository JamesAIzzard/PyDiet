import tkinter as tk
from typing import Optional

import gui
import model.quantity.validation


class RefQtyEditorWidget(tk.Frame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._ref_qty_label = tk.Label(master=self, text="Ref Quantity:")
        self.ref_qty_value_entry = gui.SmartEntryWidget(master=self, width=15, invalid_bg=gui.configs.invalid_bg_colour)
        self.ref_qty_unit_dropdown = gui.SmartDropdownWidget(master=self, width=8)
        self._ref_qty_label.grid(row=0, column=0)
        self.ref_qty_value_entry.grid(row=0, column=1)
        self.ref_qty_unit_dropdown.grid(row=0, column=2)


class DensityEditorWidget(tk.Frame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Build the UI elements;
        self._widget_label = tk.Label(master=self, text="Density:")
        self.vol_value_entry = gui.SmartEntryWidget(master=self, width=10, invalid_bg=gui.configs.invalid_bg_colour)
        self.vol_unit_dropdown = gui.SmartDropdownWidget(master=self, width=8)
        self._weighs_label = tk.Label(master=self, text=" weighs ")
        self.mass_value_entry = gui.SmartEntryWidget(master=self, width=10, invalid_bg=gui.configs.invalid_bg_colour)
        self.mass_unit_dropdown = gui.SmartDropdownWidget(master=self, width=8)
        self._widget_label.grid(row=0, column=0)
        self.vol_value_entry.grid(row=0, column=1)
        self.vol_unit_dropdown.grid(row=0, column=2)
        self._weighs_label.grid(row=0, column=3)
        self.mass_value_entry.grid(row=0, column=4)
        self.mass_unit_dropdown.grid(row=0, column=5)


class PieceMassEditorWidget(tk.Frame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Build the UI elements;
        self._widget_label = tk.Label(master=self, text="Piece Mass:")
        self.num_pieces_entry = gui.SmartEntryWidget(master=self, width=10, invalid_bg=gui.configs.invalid_bg_colour)
        self._label = tk.Label(master=self, text=" piece(s) weighs ")
        self.pieces_mass_value_entry = gui.SmartEntryWidget(
            master=self,
            width=10,
            invalid_bg=gui.configs.invalid_bg_colour
        )
        self.pieces_mass_units_dropdown = gui.SmartDropdownWidget(master=self, width=8)
        self._widget_label.grid(row=0, column=0)
        self.num_pieces_entry.grid(row=0, column=1)
        self._label.grid(row=0, column=2)
        self.pieces_mass_value_entry.grid(row=0, column=3)
        self.pieces_mass_units_dropdown.grid(row=0, column=4)


class BulkEditorWidget(tk.LabelFrame):
    def __init__(self, **kwargs):
        super().__init__(text="Bulk Properties", **kwargs)
        self.ref_quantity_widget = RefQtyEditorWidget(master=self)
        self.density_widget = DensityEditorWidget(master=self)
        self.piece_mass_widget = PieceMassEditorWidget(master=self)
        self.ref_quantity_widget.grid(row=0, column=0, sticky="w")
        self.density_widget.grid(row=1, column=0, sticky="w")
        self.piece_mass_widget.grid(row=2, column=0, sticky="w")


class HasBulkEditorWidget(gui.HasSubject):
    def __init__(self, bulk_editor_widget: 'gui.BulkEditorWidget', **kwargs):
        super().__init__(**kwargs)

        # Check the subject type has editable bulk;
        if not issubclass(self._subject_type, model.quantity.HasSettableBulk):
            raise TypeError("BulkEditorWidget requires the subject support bulk property setting.")

        self._bulk_editor_widget = bulk_editor_widget

        # Bind handlers to events;
        self._bulk_editor_widget.bind("<<Ref-Qty-Value-Changed>>", self._on_ref_qty_value_change)
        self._bulk_editor_widget.bind("<<Ref-Qty-Unit-Changed>>", self._on_ref_qty_unit_change)
        self._bulk_editor_widget.bind("<<Density-Mass-Value-Changed>>", self._on_density_mass_value_change)
        self._bulk_editor_widget.bind("<<Density-Mass-Unit-Changed>>", self._on_density_mass_unit_change)
        self._bulk_editor_widget.bind("<<Density-Vol-Value-Changed>>", self._on_density_vol_value_change)
        self._bulk_editor_widget.bind("<<Density-Vol-Unit-Changed>>", self._on_density_vol_unit_change)
        self._bulk_editor_widget.bind("<<Num-Pieces-Changed>>", self._on_piece_value_change)
        self._bulk_editor_widget.bind("<<Pieces-Mass-Value-Changed>>", self._on_piece_mass_value_change)
        self._bulk_editor_widget.bind("<<Pieces-Mass-Unit-Changed>>", self._on_piece_mass_unit_change)

    @property
    def ref_qty_value(self) -> Optional[float]:
        """Gets the reference quantity value."""
        return model.quantity.validation.validate_quantity(
            self._bulk_editor_widget.ref_qty_and_unit_widget.entry.get()
        )

    def _on_ref_qty_value_change(self, _) -> None:
        """Handles changes to the reference quantity value."""
        subject: 'model.quantity.HasSettableBulk' = self.subject
        try:
            subject.ref_qty = self.ref_qty_value
            self._bulk_editor_widget.ref_qty_and_unit_widget.make_entry_valid()
        except ValueError:
            self._bulk_editor_widget.ref_qty_and_unit_widget.make_entry_invalid()

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
