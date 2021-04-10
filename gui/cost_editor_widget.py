import tkinter as tk
from typing import List

import gui
import model


class CostEditorWidget(tk.Frame):
    """View to display/manipulate the cost of a substance per quantity."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create the components;
        self._cost_label = tk.Label(master=self, width=6, text="Cost: £", anchor="w")
        self._cost_label.grid(row=0, column=0)
        self._cost_entry = gui.SmartEntryWidget(master=self, width=10, invalid_bg=gui.configs.invalid_bg_colour)
        self._cost_entry.grid(row=0, column=1)
        self._per_label = tk.Label(master=self, text=" per ")
        self._per_label.grid(row=0, column=2)
        self._qty_entry = gui.SmartEntryWidget(master=self, width=5, invalid_bg=gui.configs.invalid_bg_colour)
        self._qty_entry.grid(row=0, column=3)
        self._qty_units_dropdown = gui.SmartDropdownWidget(master=self, width=8)
        self._qty_units_dropdown.grid(row=0, column=4)

        # Wire up events;
        self._cost_entry.bind("<<Value-Changed>>", lambda _: self.event_generate("<<Cost-Changed>>"))
        self._qty_entry.bind("<<Value-Changed>>", lambda _: self.event_generate("<<Qty-Changed>>"))
        self._qty_units_dropdown.bind("<<Value-Changed>>", lambda _: self.event_generate("<<Qty-Units-Changed>>"))

    @property
    def cost_value(self) -> float:
        """Returns the contents of the cost value entry box."""
        if self._cost_entry.get() == "":
            return 0
        else:
            return float(self._cost_entry.get())

    @property
    def subject_qty_value(self) -> float:
        """Returns the contents of the qty value entry box."""
        if self._qty_entry.get() == "":
            return 0
        else:
            return float(self._qty_entry.get())

    @property
    def subject_qty_unit(self) -> str:
        """Returns the currently selected quantity unit."""
        return self._qty_units_dropdown.get()

    @subject_qty_unit.setter
    def subject_qty_unit(self, qty_unit: str) -> None:
        """Sets the selected quantity unit."""
        self._qty_units_dropdown.set(qty_unit)

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

    def add_unit_options(self, units: List[str]) -> None:
        """Adds units to the units dropdown box."""
        self._qty_units_dropdown.add_options(units)

    def remove_unit_options(self, units: List[str]) -> None:
        """Removes units from the units dropdown box."""
        self._qty_units_dropdown.remove_options(units)


class HasCostEditorWidget(gui.HasSubject):
    def __init__(self, cost_editor_widget: 'gui.CostEditorWidget', **kwargs):
        super().__init__(**kwargs)

        # Check the subject type has editable cost;
        if not issubclass(self.subject_type, model.cost.SupportsSettableCost):
            raise TypeError("CostEditorWidget requires the subject to support cost setting.")
        self._cost_editor_widget = cost_editor_widget

        # Init the subject qty dropdown;
        self._cost_editor_widget.add_unit_options(model.quantity.get_recognised_mass_units())
        self._cost_editor_widget.subject_qty_unit = 'g'
        if self.subject is not None:
            if self.subject.density_is_defined:
                self._cost_editor_widget.add_unit_options(model.quantity.get_recognised_vol_units())
            if self.subject.piece_mass_defined:
                self._cost_editor_widget.add_unit_options(model.quantity.get_recognised_pc_units())

        # Bind handlers to widget events;
        self._cost_editor_widget.bind("<<Cost-Changed>>", self._on_cost_value_change)
        self._cost_editor_widget.bind("<<Qty-Changed>>", self._on_cost_subject_qty_value_change)
        self._cost_editor_widget.bind("<<Qty-Units-Changed>>", self._on_cost_subject_qty_unit_change)

    def _post_values(self) -> None:
        """Posts the values from the form onto the subject."""
        subject: 'model.cost.SupportsSettableCost' = self.subject
        if self._cost_editor_widget.cost_in_valid_state and self._cost_editor_widget.qty_in_valid_state:
            subject.set_cost(
                cost_gbp=self._cost_editor_widget.cost_value,
                qty=self._cost_editor_widget.subject_qty_value,
                unit=self._cost_editor_widget.subject_qty_unit
            )

    def _on_cost_value_change(self, _) -> None:
        """Handler for changes in the cost value field."""
        try:
            _ = model.cost.validation.validate_cost(self._cost_editor_widget.cost_value)
            self._cost_editor_widget.make_cost_valid()
            self._post_values()
        except (model.cost.exceptions.CostValueError, ValueError):
            self._cost_editor_widget.make_cost_invalid()

    def _on_cost_subject_qty_value_change(self, _) -> None:
        """Handler for changes in the subject quantity value field."""
        try:
            _ = model.quantity.validation.validate_quantity(self._cost_editor_widget.subject_qty_value)
            self._cost_editor_widget.make_qty_valid()
            self._post_values()
        except (model.quantity.exceptions.InvalidQtyError, ValueError):
            self._cost_editor_widget.make_qty_invalid()

    def _on_cost_subject_qty_unit_change(self, _) -> None:
        """Handler for changes in the subject quantity unit dropdown."""
        self._post_values()
