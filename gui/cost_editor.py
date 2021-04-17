import tkinter as tk
from typing import Optional

import gui
import model


class CostEditorView(tk.Frame):
    """View to display/manipulate the cost of a substance per quantity."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create the components;
        self._cost_label = tk.Label(master=self, width=6, text="Cost: £", anchor="w")
        self._cost_label.grid(row=0, column=0, sticky="w")
        self.cost_entry = gui.SmartEntryWidget(master=self, width=10, invalid_bg=gui.configs.invalid_bg_colour)
        self.cost_entry.grid(row=0, column=1)
        self._per_label = tk.Label(master=self, text=" per ")
        self._per_label.grid(row=0, column=2)
        self.qty_entry = gui.SmartEntryWidget(master=self, width=8, invalid_bg=gui.configs.invalid_bg_colour)
        self.qty_entry.grid(row=0, column=3)
        self.qty_units_dropdown = gui.SmartDropdownWidget(master=self, width=8)
        self.qty_units_dropdown.grid(row=0, column=4)


class CostEditorController(gui.HasSubject, gui.SupportsDefinition, gui.SupportsValidity):

    def __init__(self, view: 'gui.CostEditorView', **kwargs):
        super().__init__(view=view, subject_type=model.cost.SupportsSettableCost, **kwargs)
        self.view.cost_entry.bind("<<Value-Changed>>", self.process_view_changes)
        self.view.qty_entry.bind("<<Value-Changed>>", self.process_view_changes)
        self.view.qty_units_dropdown.bind("<<Value-Changed>>", self.process_view_changes)

    @property
    def cost_value(self) -> Optional[float]:
        """Returns the cost value."""
        return gui.get_noneable_qty_entry(self.view.cost_entry)

    @cost_value.setter
    def cost_value(self, cost_value: Optional[float]) -> None:
        """Sets the cost value."""
        gui.set_noneable_qty_entry(self.view.cost_entry, cost_value)

    @property
    def cost_qty_value(self) -> Optional[float]:
        """Returns the cost quantity value."""
        return gui.get_noneable_qty_entry(self.view.qty_entry)

    @cost_qty_value.setter
    def cost_qty_value(self, cost_qty_value: Optional[float]) -> None:
        """Sets the cost quantity value."""
        gui.set_noneable_qty_entry(self.view.qty_entry, cost_qty_value)

    @property
    def cost_qty_unit(self) -> str:
        """Gets the cost quantity unit."""
        return self.view.qty_units_dropdown.get()

    @cost_qty_unit.setter
    def cost_qty_unit(self, cost_qty_unit: str) -> None:
        """Sets the cost quantity unit."""
        self.view.qty_units_dropdown.set(cost_qty_unit)

    @property
    def is_defined(self) -> bool:
        return gui.entry_is_defined(self.view.cost_entry) and gui.entry_is_defined(self.view.qty_entry)

    @property
    def is_valid(self) -> bool:
        if not self.view.cost_entry.is_valid:
            return False
        if not self.view.qty_entry.is_valid:
            return False
        return True

    @property
    def subject(self) -> 'model.cost.SupportsSettableCost':
        return super().subject

    def set_subject(self, subject: 'model.cost.SupportsSettableCost') -> None:
        super().set_subject(subject)

    def update_view(self) -> None:
        # Catch empty subject;
        if self.subject is None:
            return

        if self.subject.cost_per_g_defined:
            self.cost_value = round(self.subject.cost_of_ref_qty, 4)
        self.cost_qty_value = round(self.subject.ref_qty, 2)
        gui.configure_qty_units(self.view.qty_units_dropdown, self.subject)
        self.cost_qty_unit = self.subject.pref_unit

    def process_view_changes(self, _) -> None:
        """Handler for view changes."""
        gui.validate_qty_entry(self.view.cost_entry)
        gui.validate_qty_entry(self.view.qty_entry)
        if self.is_defined and self.is_valid:
            self.subject.set_cost(
                cost_gbp=self.cost_value,
                qty=self.cost_qty_value,
                unit=self.cost_qty_unit
            )

    @property
    def view(self) -> 'gui.CostEditorView':
        view = super().view
        assert (isinstance(view, gui.CostEditorView))
        return view
