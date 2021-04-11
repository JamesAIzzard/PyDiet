import tkinter as tk
from typing import Optional

import gui
import model


class CostEditorWidget(tk.Frame):
    """View to display/manipulate the cost of a substance per quantity."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create the components;
        self._cost_label = tk.Label(master=self, width=6, text="Cost: £", anchor="w")
        self._cost_label.grid(row=0, column=0)
        self.cost_entry = gui.SmartEntryWidget(master=self, width=10, invalid_bg=gui.configs.invalid_bg_colour)
        self.cost_entry.grid(row=0, column=1)
        self._per_label = tk.Label(master=self, text=" per ")
        self._per_label.grid(row=0, column=2)
        self.qty_entry = gui.SmartEntryWidget(master=self, width=5, invalid_bg=gui.configs.invalid_bg_colour)
        self.qty_entry.grid(row=0, column=3)
        self.qty_units_dropdown = gui.SmartDropdownWidget(master=self, width=8)
        self.qty_units_dropdown.grid(row=0, column=4)


class HasCostEditorWidget(gui.HasSubject):
    def __init__(self, cost_editor_widget: 'gui.CostEditorWidget', **kwargs):
        super().__init__(**kwargs)

        # Check the subject type has editable cost;
        if not issubclass(self._subject_type, model.cost.SupportsSettableCost):
            raise TypeError("CostEditorWidget requires the subject to support cost setting.")

        # Stash the view;
        self._cost_editor_widget = cost_editor_widget

        # Init the subject qty dropdown;
        self._config_qty_units()

        # Bind handlers to widget events;
        self._cost_editor_widget.cost_entry.bind("<<Value-Changed>>", self._on_cost_value_change)
        self._cost_editor_widget.qty_entry.bind("<<Value-Changed>>", self._on_cost_subject_qty_value_change)
        self._cost_editor_widget.qty_units_dropdown.bind("<<Value-Changed>>", self._on_cost_subject_qty_unit_change)

    def _config_qty_units(self) -> None:
        """Configues the units in the qty dropdown."""
        self._cost_editor_widget.qty_units_dropdown.remove_options()
        self._cost_editor_widget.qty_units_dropdown.add_options(model.quantity.get_recognised_mass_units())
        self._cost_editor_widget.subject_qty_unit = 'g'
        if self.subject is not None:
            if self.subject.density_is_defined:
                self._cost_editor_widget.qty_units_dropdown.add_options(model.quantity.get_recognised_vol_units())
            if self.subject.piece_mass_defined:
                self._cost_editor_widget.qty_units_dropdown.add_options(model.quantity.get_recognised_pc_units())

    @property
    def cost_value(self) -> Optional[float]:
        if self._cost_editor_widget.cost_entry.get() == "":
            return None
        else:
            return float(self._cost_editor_widget.cost_entry.get())

    @property
    def subject_qty_value(self) -> Optional[float]:
        if self._cost_editor_widget.qty_entry.get() == "":
            return None
        else:
            return float(self._cost_editor_widget.qty_entry.get())

    @property
    def subject_qty_unit(self) -> str:
        return self._cost_editor_widget.qty_units_dropdown.get()

    def _set_subject(self, subject: 'model.cost.SupportsSettableCost') -> None:
        # Configure the qty units;
        self._config_qty_units()
        # Set the widget values;
        if subject.cost_per_g is not None:
            self._cost_editor_widget.cost_entry.set(str(subject.cost_per_pref_unit))
        self._cost_editor_widget.qty_entry.set(str(subject.ref_qty))
        self._cost_editor_widget.qty_units_dropdown.set(subject.pref_unit)
        super()._set_subject(subject)

    def _post_values(self) -> None:
        """Posts the values from the form onto the subject."""
        subject: Optional['model.cost.SupportsSettableCost'] = self.subject
        if subject is None:
            return
        if self._cost_editor_widget.cost_entry.in_valid_state and self._cost_editor_widget.qty_entry.in_valid_state:
            subject.set_cost(
                cost_gbp=self.cost_value,
                qty=self.subject_qty_value,
                unit=self.subject_qty_unit
            )

    def _on_cost_value_change(self, _) -> None:
        """Handler for changes in the cost value field."""
        try:
            _ = model.cost.validation.validate_cost(self.cost_value)
            self._cost_editor_widget.cost_entry.make_valid()
            self._post_values()
        except (model.cost.exceptions.CostValueError, ValueError):
            self._cost_editor_widget.cost_entry.make_invalid()

    def _on_cost_subject_qty_value_change(self, _) -> None:
        """Handler for changes in the subject quantity value field."""
        try:
            _ = model.quantity.validation.validate_quantity(self.subject_qty_value)
            self._cost_editor_widget.cost_entry.make_valid()
            self._post_values()
        except (model.quantity.exceptions.InvalidQtyError, ValueError):
            self._cost_editor_widget.cost_entry.make_invalid()

    def _on_cost_subject_qty_unit_change(self, _) -> None:
        """Handler for changes to the subject qty units dropdown."""
        self._post_values()
