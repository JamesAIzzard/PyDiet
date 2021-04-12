import tkinter as tk

import gui
import model


class CostEditorView(tk.Frame):
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
        self.qty_entry = gui.SmartEntryWidget(master=self, width=8, invalid_bg=gui.configs.invalid_bg_colour)
        self.qty_entry.grid(row=0, column=3)
        self.qty_units_dropdown = gui.SmartDropdownWidget(master=self, width=8)
        self.qty_units_dropdown.grid(row=0, column=4)


class CostEditorController(gui.HasSubject):
    def __init__(self, view: 'gui.CostEditorView', **kwargs):
        super().__init__(view=view, subject_type=model.cost.SupportsSettableCost, **kwargs)
        self.view.cost_entry.bind("<<Value-Changed>>", self.process_view_changes)
        self.view.qty_entry.bind("<<Value-Changed>>", self.process_view_changes)
        self.view.qty_units_dropdown.bind("<<Value-Changed>>", self.process_view_changes)

    @property
    def subject(self) -> 'model.cost.SupportsSettableCost':
        return super().subject

    def set_subject(self, subject: 'model.cost.SupportsSettableCost') -> None:
        super().set_subject(subject)

    def update_view(self) -> None:
        if self.subject.cost_per_g_defined:
            self.view.cost_entry.set(str(self.subject.cost_of_ref_qty))
        self.view.qty_entry.set(str(self.subject.ref_qty))
        gui.configure_qty_units(self.view.qty_units_dropdown, self.subject)
        self.view.qty_units_dropdown.set(self.subject.pref_unit)

    def process_view_changes(self, _) -> None:
        # Work through and validate the view;
        should_set: bool = True  # Indicates if setting should go ahead;
        # Try and collect the cost value first;
        try:
            cost_value = self.view.cost_entry.get()
            if cost_value == "":
                cost_value = None
            else:
                cost_value = model.cost.validation.validate_cost(float(cost_value))
            self.view.cost_entry.make_valid()
        except (ValueError, model.cost.exceptions.CostValueError):
            self.view.cost_entry.make_invalid()
            cost_value = None
            should_set = False
        # Now try the qty value;
        try:
            qty_value = self.view.qty_entry.get()
            if qty_value == "":
                qty_value = None
            else:
                qty_value = model.quantity.validation.validate_quantity(float(qty_value))
            self.view.qty_entry.make_valid()
        except (ValueError, model.quantity.exceptions.InvalidQtyError):
            self.view.qty_entry.make_invalid()
            qty_value = None
            should_set = False

        # If the view validated OK, use the values to set the subject;
        if should_set:
            if cost_value is None or qty_value is None:
                self.subject.cost_per_g = None
            else:
                self.subject.set_cost(
                    cost_gbp=cost_value,
                    qty=qty_value,
                    unit=self.view.qty_units_dropdown.get()
                )

    @property
    def view(self) -> 'gui.CostEditorView':
        view = super().view
        assert (isinstance(view, gui.CostEditorView))
        return view
