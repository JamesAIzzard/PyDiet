import tkinter as tk
from tkinter import messagebox
from typing import Optional

import gui
import model.quantity.validation


class RefQtyEditorView(tk.Frame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._ref_qty_label = tk.Label(master=self, text="Ref Quantity:", width=10, anchor="w")
        self.ref_qty_value_entry = gui.SmartEntryWidget(master=self, width=15, invalid_bg=gui.configs.invalid_bg_colour)
        self.ref_qty_unit_dropdown = gui.SmartDropdownWidget(master=self, width=8)
        self._ref_qty_label.grid(row=0, column=0)
        self.ref_qty_value_entry.grid(row=0, column=1)
        self.ref_qty_unit_dropdown.grid(row=0, column=2)


class RefQtyEditorController(gui.HasSubject, gui.SupportsValidity, gui.SupportsDefinition):
    def __init__(self, view: 'RefQtyEditorView', **kwargs):
        super().__init__(subject_type=model.quantity.HasSettableBulk, view=view, **kwargs)
        self.view.ref_qty_value_entry.bind("<<Value-Changed>>", self.process_view_changes)
        self.view.ref_qty_unit_dropdown.bind("<<Value-Changed>>", self.process_view_changes)

    @property
    def ref_qty_value(self) -> Optional[float]:
        """Gets the reference qty value."""
        return gui.get_noneable_qty_entry(self.view.ref_qty_value_entry)

    @ref_qty_value.setter
    def ref_qty_value(self, ref_qty_value: Optional[float]) -> None:
        """Sets the reference qty value."""
        gui.set_noneable_qty_entry(self.view.ref_qty_value_entry, round(ref_qty_value, 2))

    @property
    def pref_unit(self) -> str:
        """Gets the req qty unit dropdown."""
        return self.view.ref_qty_unit_dropdown.get()

    @pref_unit.setter
    def pref_unit(self, pref_unit: str) -> None:
        """Sets the reference quantity unit."""
        self.view.ref_qty_unit_dropdown.set(pref_unit)

    @property
    def is_valid(self) -> bool:
        return self.view.ref_qty_value_entry.is_valid

    @property
    def is_defined(self) -> bool:
        return gui.entry_is_defined(self.view.ref_qty_value_entry)

    @property
    def subject(self) -> 'model.quantity.HasSettableBulk':
        return super().subject

    def set_subject(self, subject: 'model.quantity.HasSettableBulk') -> None:
        super().set_subject(subject)

    @property
    def view(self) -> 'RefQtyEditorView':
        view = super().view
        assert (isinstance(view, RefQtyEditorView))
        return view

    def update_view(self) -> None:
        # Catch empty subject;
        if self.subject is None:
            return

        self.ref_qty_value = self.subject.ref_qty
        gui.configure_qty_units(self.view.ref_qty_unit_dropdown, self.subject)
        self.pref_unit = self.subject.qty_pref_unit

    def process_view_changes(self, *args, **kwargs) -> None:
        gui.validate_nonzero_qty_entry(self.view.ref_qty_value_entry)
        if self.is_defined and self.is_valid:
            self.subject.ref_qty = self.ref_qty_value
            self.subject.qty_pref_unit = self.pref_unit
            # Emit event to indicate ref qty was changed.
            self.view.event_generate("<<Ref-Qty-Changed>>")


class DensityEditorView(tk.Frame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Build the UI elements;
        self._widget_label = tk.Label(master=self, text="Density:", width=10, anchor="w")
        self.vol_value_entry = gui.SmartEntryWidget(master=self, width=10, invalid_bg=gui.configs.invalid_bg_colour)
        self.vol_unit_dropdown = gui.SmartDropdownWidget(master=self, width=8)
        self._weighs_label = tk.Label(master=self, text=" weighs ")
        self.mass_value_entry = gui.SmartEntryWidget(master=self, width=10, invalid_bg=gui.configs.invalid_bg_colour)
        self.mass_unit_dropdown = gui.SmartDropdownWidget(master=self, width=8)
        self.set_button = tk.Button(master=self, text="Set")
        self.clear_button = tk.Button(master=self, text="Clear")
        self._widget_label.grid(row=0, column=0)
        self.vol_value_entry.grid(row=0, column=1)
        self.vol_unit_dropdown.grid(row=0, column=2)
        self._weighs_label.grid(row=0, column=3)
        self.mass_value_entry.grid(row=0, column=4)
        self.mass_unit_dropdown.grid(row=0, column=5)
        self.set_button.grid(row=0, column=6)
        self.clear_button.grid(row=0, column=7)


class DensityEditorController(gui.HasSubject, gui.SupportsValidity, gui.SupportsDefinition):
    def __init__(self, view: 'DensityEditorView', **kwargs):
        super().__init__(subject_type=model.quantity.HasSettableBulk, view=view, **kwargs)

        # Configure the dropdowns;
        self.view.vol_unit_dropdown.add_options(model.quantity.get_recognised_vol_units())
        self.view.vol_unit_dropdown.set("ml")
        self.view.mass_unit_dropdown.add_options(model.quantity.get_recognised_mass_units())
        self.view.mass_unit_dropdown.set("g")

        # Bind to view changes;
        self.view.vol_value_entry.bind("<<Value-Changed>>", self.process_view_changes)
        self.view.mass_value_entry.bind("<<Value-Changed>>", self.process_view_changes)
        self.view.set_button.bind("<Button-1>", self._on_set_density)
        self.view.clear_button.bind("<Button-1>", self._on_clear_density)

    @property
    def vol_value(self) -> Optional[float]:
        """Gets the volume value."""
        return gui.get_noneable_qty_entry(self.view.vol_value_entry)

    @vol_value.setter
    def vol_value(self, vol_value: Optional[float]) -> None:
        """Sets the volume value."""
        gui.set_noneable_qty_entry(self.view.vol_value_entry, vol_value)

    @property
    def vol_unit(self) -> str:
        """Returns the volume unit."""
        return self.view.vol_unit_dropdown.get()

    @vol_unit.setter
    def vol_unit(self, vol_unit: str) -> None:
        """Sets the volume unit."""
        self.view.vol_unit_dropdown.set(vol_unit)

    @property
    def mass_value(self) -> Optional[float]:
        """Gets the mass value."""
        return gui.get_noneable_qty_entry(self.view.mass_value_entry)

    @mass_value.setter
    def mass_value(self, mass_value: Optional[float]) -> None:
        """Sets the mass value."""
        gui.set_noneable_qty_entry(self.view.mass_value_entry, mass_value)

    @property
    def mass_unit(self) -> str:
        """Returns the mass unit."""
        return self.view.mass_unit_dropdown.get()

    @mass_unit.setter
    def mass_unit(self, mass_unit: str) -> None:
        """Sets the mass unit."""
        self.view.mass_unit_dropdown.set(mass_unit)

    @property
    def is_valid(self) -> bool:
        return self.view.vol_value_entry.is_valid and self.view.mass_value_entry.is_valid

    @property
    def is_defined(self) -> bool:
        return gui.entry_is_defined(self.view.vol_value_entry) and gui.entry_is_defined(self.view.mass_value_entry)

    @property
    def subject(self) -> 'model.quantity.HasSettableBulk':
        return super().subject

    def set_subject(self, subject: 'model.quantity.HasSettableBulk') -> None:
        super().set_subject(subject)

    @property
    def view(self) -> 'DensityEditorView':
        return super().view

    def update_view(self) -> None:
        if self.subject.density_is_defined:
            self.vol_value = 100
            self.view.vol_unit_dropdown.set("ml")
            self.mass_value = self.subject.g_per_ml * 100
            self.view.mass_unit_dropdown.set("g")

    def _on_set_density(self, _) -> None:
        """Handler for press on density set."""
        # Catch invalid fields.
        if self.is_invalid:
            messagebox.showinfo(title="PyDiet", message="Density fields are invald.")
            self.update_view()  # Return view back to model.
            return

        # Catch unsetting when density is in use;
        if self.mass_value is None or self.vol_value is None:
            if self.subject.density_units_in_use:
                messagebox.showinfo(title="PyDiet", message="Cannot unset density, density values are in use.")
                self.update_view()  # Return view back to model.
                return

        # All OK, go ahead;
        self.subject.set_density(
            mass_qty=self.mass_value,
            mass_unit=self.mass_unit,
            vol_qty=self.vol_value,
            vol_unit=self.vol_unit
        )
        self.view.event_generate("<<Density-Changed>>")

    def _on_clear_density(self, event) -> None:
        """Handler for press on the clear button."""
        self.vol_value = None
        self.mass_value = None
        self._on_set_density(event)

    def process_view_changes(self, *args, **kwargs) -> None:
        gui.validate_nonzero_qty_entry(self.view.mass_value_entry)
        gui.validate_nonzero_qty_entry(self.view.vol_value_entry)


class PieceMassEditorView(tk.Frame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Build the UI elements;
        self._widget_label = tk.Label(master=self, text="Piece Mass:", width=10, anchor="w")
        self.num_pieces_entry = gui.SmartEntryWidget(master=self, width=10, invalid_bg=gui.configs.invalid_bg_colour)
        self._label = tk.Label(master=self, text=" piece(s) weighs ")
        self.pieces_mass_value_entry = gui.SmartEntryWidget(
            master=self,
            width=10,
            invalid_bg=gui.configs.invalid_bg_colour
        )
        self.pieces_mass_units_dropdown = gui.SmartDropdownWidget(master=self, width=8)
        self.set_button = tk.Button(master=self, text="Set")
        self.clear_button = tk.Button(master=self, text="Clear")

        # Place the elements;
        self._widget_label.grid(row=0, column=0)
        self.num_pieces_entry.grid(row=0, column=1)
        self._label.grid(row=0, column=2)
        self.pieces_mass_value_entry.grid(row=0, column=3)
        self.pieces_mass_units_dropdown.grid(row=0, column=4)
        self.set_button.grid(row=0, column=5)
        self.clear_button.grid(row=0, column=6)


class PieceMassEditorController(gui.HasSubject, gui.SupportsValidity, gui.SupportsDefinition):
    def __init__(self, view: 'PieceMassEditorView', **kwargs):
        super().__init__(subject_type=model.quantity.HasSettableBulk, view=view, **kwargs)

        # Populate the units dropdown;
        self.view.pieces_mass_units_dropdown.add_options(model.quantity.get_recognised_mass_units())
        self.piece_mass_units = 'g'  # Init as grams.

        self.view.num_pieces_entry.bind("<<Value-Changed>>", self.process_view_changes)
        self.view.pieces_mass_value_entry.bind("<<Value-Changed>>", self.process_view_changes)
        self.view.set_button.bind("<Button-1>", self._on_set_pc_mass)
        self.view.clear_button.bind("<Button-1>", self._on_clear_pc_mass)

    @property
    def num_pieces(self) -> Optional[float]:
        """Gets the number of pieces."""
        return gui.get_noneable_qty_entry(self.view.num_pieces_entry)

    @num_pieces.setter
    def num_pieces(self, num_pieces: Optional[float]) -> None:
        """Sets the number of pieces."""
        gui.set_noneable_qty_entry(self.view.num_pieces_entry, num_pieces)

    @property
    def pieces_mass(self) -> Optional[float]:
        """Gets the mass of the pieces."""
        return gui.get_noneable_qty_entry(self.view.pieces_mass_value_entry)

    @pieces_mass.setter
    def pieces_mass(self, pieces_mass: Optional[float]) -> None:
        """Sets the mass of the pieces."""
        gui.set_noneable_qty_entry(self.view.pieces_mass_value_entry, pieces_mass)

    @property
    def piece_mass_units(self) -> str:
        """Gets the piece mass units."""
        return self.view.pieces_mass_units_dropdown.get()

    @piece_mass_units.setter
    def piece_mass_units(self, units: str) -> None:
        """Sets the piece mass units."""
        self.view.pieces_mass_units_dropdown.set(units)

    @property
    def is_valid(self) -> bool:
        return self.view.pieces_mass_value_entry.is_valid and self.view.num_pieces_entry.is_valid

    @property
    def is_defined(self) -> bool:
        return gui.entry_is_defined(self.view.pieces_mass_value_entry) and gui.entry_is_defined(
            self.view.num_pieces_entry)

    @property
    def subject(self) -> 'model.quantity.HasSettableBulk':
        return super().subject

    def set_subject(self, subject: 'model.quantity.HasSettableBulk') -> None:
        super().set_subject(subject)

    @property
    def view(self) -> 'PieceMassEditorView':
        return super().view

    def update_view(self) -> None:
        if self.subject.piece_mass_is_defined:
            self.num_pieces = 1
            if model.quantity.units_are_masses(self.subject.qty_pref_unit):
                self.pieces_mass = self.subject.piece_mass_in_pref_units
                self.piece_mass_units = self.subject.qty_pref_unit
            else:
                self.pieces_mass = self.subject.piece_mass_g
                self.piece_mass_units = 'g'
        else:
            self.num_pieces = None
            self.pieces_mass = None
            self.piece_mass_units = 'g'

    def _on_set_pc_mass(self, _) -> None:
        """Handler for press on pc mass set."""
        # Catch invalid fields;
        if self.is_invalid:
            messagebox.showinfo(title="PyDiet", message="Piece mass fields are invalid.")
            self.update_view()  # Return view back to model
            return

        # Catch unsetting when pc mas is in use;
        if self.num_pieces is None or self.pieces_mass is None:
            if self.subject.piece_mass_units_in_use:
                messagebox.showinfo(title="PyDiet", message="Cannot unset piece mass, piece unit is in use.")
                self.update_view() # Return view back to model
                return

        # All OK, go ahead;
        self.subject.set_piece_mass(
            num_pieces=self.num_pieces,
            mass_qty=self.pieces_mass,
            mass_unit=self.piece_mass_units
        )
        self.view.event_generate("<<Piece-Mass-Changed>>")

    def _on_clear_pc_mass(self, event) -> None:
        self.pieces_mass = None
        self.num_pieces = None
        self._on_set_pc_mass(event)

    def process_view_changes(self, *args, **kwargs) -> None:
        gui.validate_nonzero_qty_entry(self.view.pieces_mass_value_entry)
        gui.validate_nonzero_qty_entry(self.view.num_pieces_entry)


class BulkEditorView(tk.LabelFrame):
    def __init__(self, **kwargs):
        super().__init__(text="Bulk Properties", **kwargs)
        self.ref_quantity_editor = RefQtyEditorView(master=self)
        self.density_editor = DensityEditorView(master=self)
        self.piece_mass_editor = PieceMassEditorView(master=self)
        self.ref_quantity_editor.grid(row=0, column=0, sticky="w")
        self.density_editor.grid(row=1, column=0, sticky="w")
        self.piece_mass_editor.grid(row=2, column=0, sticky="w")


class BulkEditorController(gui.HasSubject):
    def __init__(self, view: 'gui.BulkEditorView', **kwargs):
        super().__init__(view=view, subject_type=model.quantity.HasSettableBulk, **kwargs)

        # Child controllers;
        self.ref_qty_editor = RefQtyEditorController(view=view.ref_quantity_editor, **kwargs)
        self.density_editor = DensityEditorController(view=view.density_editor, **kwargs)
        self.piece_mass_editor = PieceMassEditorController(view=view.piece_mass_editor, **kwargs)

    @property
    def subject(self) -> 'model.quantity.HasSettableBulk':
        return super().subject

    def set_subject(self, subject: 'model.quantity.HasSettableBulk') -> None:
        self.ref_qty_editor.set_subject(subject)
        self.density_editor.set_subject(subject)
        self.piece_mass_editor.set_subject(subject)
        super().set_subject(subject)

    @property
    def view(self) -> 'BulkEditorView':
        view = super().view
        assert (isinstance(view, gui.BulkEditorView))
        return view

    def update_view(self) -> None:
        # Catch empty subject;
        if self.subject is None:
            return

        self.ref_qty_editor.update_view()
        self.density_editor.update_view()
        self.piece_mass_editor.update_view()

    def process_view_changes(self, *args, **kwargs) -> None:
        self.ref_qty_editor.process_view_changes()
        self.density_editor.process_view_changes()
        self.piece_mass_editor.process_view_changes()
