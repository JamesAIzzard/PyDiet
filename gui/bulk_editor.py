import tkinter as tk

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


class RefQtyEditorController(gui.HasSubject):
    def __init__(self, view: 'RefQtyEditorView', **kwargs):
        super().__init__(subject_type=model.quantity.HasSettableBulk, view=view, **kwargs)
        self.view.ref_qty_value_entry.bind("<<Value-Changed>>", self.process_view_changes)
        self.view.ref_qty_unit_dropdown.bind("<<Value-Changed>>", self.process_view_changes)

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
        self.view.ref_qty_value_entry.set(str(self.subject.ref_qty))
        gui.configure_qty_units(self.view.ref_qty_unit_dropdown, self.subject)
        self.view.ref_qty_unit_dropdown.set(self.subject.pref_unit)

    def process_view_changes(self, *args, **kwargs) -> None:
        ref_qty_value = self.view.ref_qty_value_entry.get()
        try:
            ref_qty_value = model.quantity.validation.validate_quantity(float(ref_qty_value))
        except (ValueError, model.quantity.exceptions.InvalidQtyError):
            self.view.ref_qty_value_entry.make_invalid()
            return
        self.subject.ref_qty = ref_qty_value
        self.subject.pref_unit = self.view.ref_qty_unit_dropdown.get()
        self.view.ref_qty_value_entry.make_valid()


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
        self._widget_label.grid(row=0, column=0)
        self.vol_value_entry.grid(row=0, column=1)
        self.vol_unit_dropdown.grid(row=0, column=2)
        self._weighs_label.grid(row=0, column=3)
        self.mass_value_entry.grid(row=0, column=4)
        self.mass_unit_dropdown.grid(row=0, column=5)


class DensityEditorController(gui.HasSubject):
    def __init__(self, view: 'DensityEditorView', **kwargs):
        super().__init__(subject_type=model.quantity.HasSettableBulk, view=view, **kwargs)
        self.view.vol_value_entry.bind("<<Value-Changed>>", self.process_view_changes)
        self.view.vol_unit_dropdown.bind("<<Value-Changed>>", self.process_view_changes)
        self.view.mass_value_entry.bind("<<Value-Changed>>", self.process_view_changes)
        self.view.mass_unit_dropdown.bind("<<Value-Changed>>", self.process_view_changes)

    @property
    def subject(self) -> 'model.quantity.HasSettableBulk':
        return super().subject

    def set_subject(self, subject: 'model.quantity.HasSettableBulk') -> None:
        super().set_subject(subject)

    @property
    def view(self) -> 'DensityEditorView':
        view = super().view
        assert (isinstance(view, DensityEditorView))
        return view

    def update_view(self) -> None:
        self.view.vol_unit_dropdown.add_options(model.quantity.get_recognised_vol_units())
        self.view.vol_unit_dropdown.set("ml")
        self.view.mass_unit_dropdown.add_options(model.quantity.get_recognised_mass_units())
        self.view.mass_unit_dropdown.set("g")
        if self.subject.density_is_defined:
            self.view.vol_value_entry.set(str(100))
            self.view.mass_value_entry.set(str(self.subject.g_per_ml * 100))

    def process_view_changes(self, *args, **kwargs) -> None:
        found_invalid = False # noqa
        # Validate the entry widgets;
        found_invalid, vol_value = gui.validate_nullable_entry(
            entry=self.view.vol_value_entry,
            validator=lambda val: model.quantity.validation.validate_quantity(float(val)),
            exceptions=(ValueError, model.quantity.exceptions.InvalidQtyError),
            found_invalid=found_invalid
        )
        found_invalid, mass_value = gui.validate_nullable_entry(
            entry=self.view.mass_value_entry,
            validator=lambda val: model.quantity.validation.validate_quantity(float(val)),
            exceptions=(ValueError, model.quantity.exceptions.InvalidQtyError),
            found_invalid=found_invalid
        )

        if not found_invalid:
            # Handle special case were both are None;
            if vol_value is None and mass_value is None:
                self.subject.g_per_ml = None
                return
            # Handle special case where one is None and the other is valid;
            elif vol_value is None or mass_value is None:
                return

            self.subject.set_density(
                mass_qty=mass_value,
                mass_unit=self.view.mass_unit_dropdown.get(),
                vol_qty=vol_value,
                vol_unit=self.view.vol_unit_dropdown.get()
            )


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
        self._widget_label.grid(row=0, column=0)
        self.num_pieces_entry.grid(row=0, column=1)
        self._label.grid(row=0, column=2)
        self.pieces_mass_value_entry.grid(row=0, column=3)
        self.pieces_mass_units_dropdown.grid(row=0, column=4)


class PieceMassEditorController(gui.HasSubject):
    def __init__(self, view: 'PieceMassEditorView', **kwargs):
        super().__init__(subject_type=model.quantity.HasSettableBulk, view=view, **kwargs)
        self.view.num_pieces_entry.bind("<<Value-Changed>>", self.process_view_changes)
        self.view.pieces_mass_value_entry.bind("<<Value-Changed>>", self.process_view_changes)
        self.view.pieces_mass_units_dropdown.bind("<<Value-Changed>>", self.process_view_changes)

    @property
    def subject(self) -> 'model.quantity.HasSettableBulk':
        return super().subject

    def set_subject(self, subject: 'model.quantity.HasSettableBulk') -> None:
        super().set_subject(subject)

    @property
    def view(self) -> 'PieceMassEditorView':
        view = super().view
        assert (isinstance(view, PieceMassEditorView))
        return view

    def update_view(self) -> None:
        # Configure the number of peices;
        self.view.num_pieces_entry.set(str(1))
        # Configure piece mass entry;
        if self.subject.piece_mass_defined:
            self.view.pieces_mass_value_entry.set(str(self.subject.piece_mass_in_pref_units))
        # Configure the piece mass unit dropdown.
        self.view.pieces_mass_units_dropdown.add_options(model.quantity.get_recognised_mass_units())
        if self.subject.pref_unit in model.quantity.get_recognised_mass_units():
            self.view.pieces_mass_units_dropdown.set(self.subject.pref_unit)
        else:
            self.view.pieces_mass_units_dropdown.set('g')

    def process_view_changes(self, *args, **kwargs) -> None:
        found_invalid = False  # noqa
        found_invalid, num_pieces_value = gui.validate_nullable_entry(
            entry=self.view.num_pieces_entry,
            validator=lambda val: model.quantity.validation.validate_quantity(float(val)),
            exceptions=(ValueError, model.quantity.exceptions.InvalidQtyError),
            found_invalid=found_invalid
        )
        found_invalid, pieces_mass_value = gui.validate_nullable_entry(
            entry=self.view.pieces_mass_value_entry,
            validator=lambda val: model.quantity.validation.validate_quantity(float(val)),
            exceptions=(ValueError, model.quantity.exceptions.InvalidQtyError),
            found_invalid=found_invalid
        )
        if not found_invalid:
            if num_pieces_value is None and pieces_mass_value is None:
                self.subject.piece_mass_g = None
                return
            elif num_pieces_value is None or pieces_mass_value is None:
                return
            self.subject.set_piece_mass(
                num_pieces=num_pieces_value,
                mass_qty=pieces_mass_value,
                mass_unit=self.view.pieces_mass_units_dropdown.get()
            )


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
        self.ref_qty_editor_controller = RefQtyEditorController(view=view.ref_quantity_editor, **kwargs)
        self.density_editor_controller = DensityEditorController(view=view.density_editor, **kwargs)
        self.piece_mass_editor_controller = PieceMassEditorController(view=view.piece_mass_editor, **kwargs)

    @property
    def subject(self) -> 'model.quantity.HasSettableBulk':
        return super().subject

    def set_subject(self, subject: 'model.quantity.HasSettableBulk') -> None:
        self.ref_qty_editor_controller.set_subject(subject)
        self.density_editor_controller.set_subject(subject)
        self.piece_mass_editor_controller.set_subject(subject)
        super().set_subject(subject)

    @property
    def view(self) -> 'BulkEditorView':
        view = super().view
        assert (isinstance(view, gui.BulkEditorView))
        return view

    def update_view(self) -> None:
        pass

    def process_view_changes(self, *args, **kwargs) -> None:
        pass
