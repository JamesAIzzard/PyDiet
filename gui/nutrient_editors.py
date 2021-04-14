import tkinter as tk
from typing import List, Dict, Callable, Optional

import gui
import model


class NutrientRatioEditorView(tk.Frame):
    """Widget to allow editing of a single nutrient ratio."""

    def __init__(self, nutrient_name: str, nutrient_display_name: str, **kwargs):
        super().__init__(**kwargs)
        self.nutrient_name = nutrient_name
        # Init the widgets;
        self._nutrient_name_label = tk.Label(master=self, text=f"{nutrient_display_name} :", width=20, anchor="w")
        self.nutrient_mass_value_entry = gui.SmartEntryWidget(master=self, width=8,
                                                              invalid_bg=gui.configs.invalid_bg_colour)
        self.nutrient_mass_unit_dropdown = gui.SmartDropdownWidget(master=self, width=8)
        self._in_label = tk.Label(master=self, text=" in ")
        self.subject_qty_value_entry = gui.SmartEntryWidget(master=self, width=8,
                                                            invalid_bg=gui.configs.invalid_bg_colour)
        self.subject_qty_unit_dropdown = gui.SmartDropdownWidget(master=self, width=8)
        self._nutrient_name_label.grid(row=0, column=0, sticky="w")
        # Pack the widgets;
        self._nutrient_name_label.grid(row=0, column=0)
        self.nutrient_mass_value_entry.grid(row=0, column=1)
        self.nutrient_mass_unit_dropdown.grid(row=0, column=2)
        self._in_label.grid(row=0, column=3)
        self.subject_qty_value_entry.grid(row=0, column=4)
        self.subject_qty_unit_dropdown.grid(row=0, column=5)


class NutrientRatioEditorController(gui.BaseController):
    def __init__(self, view: 'NutrientRatioEditorView', **kwargs):
        super().__init__(view, **kwargs)

        # Populate the nutrient mass dropdown (these don't change)
        self.view.nutrient_mass_unit_dropdown.add_options(model.quantity.get_recognised_mass_units())

        # Bind change handler;
        self.view.nutrient_mass_value_entry.bind("<<Value-Changed>>", self.process_view_changes)
        self.view.nutrient_mass_unit_dropdown.bind("<<Value-Changed>>", self.process_view_changes)
        self.view.subject_qty_value_entry.bind("<<Value-Changed>>", self.process_view_changes)
        self.view.subject_qty_unit_dropdown.bind("<<Value-Changed>>", self.process_view_changes)

    @property
    def view(self) -> 'NutrientRatioEditorView':
        return super().view

    def update_view(self,
                    nutrient_mass_value: Optional[float],
                    nutrient_mass_unit: str,
                    subject_qty_value: Optional[float],
                    subject_qty_unit: str,
                    subject_qty_available_units: List[str]
                    ) -> None:
        # Map input datatypes;
        if nutrient_mass_value is None:
            nutrient_mass_value = ""
        else:
            nutrient_mass_value = str(nutrient_mass_value)
        if subject_qty_value is None:
            subject_qty_value = ""
        else:
            subject_qty_value = str(subject_qty_value)
        self.view.nutrient_mass_value_entry.set(nutrient_mass_value)
        self.view.nutrient_mass_unit_dropdown.set(nutrient_mass_unit)
        self.view.subject_qty_value_entry.set(subject_qty_value)
        self.view.subject_qty_unit_dropdown.remove_options()
        self.view.subject_qty_unit_dropdown.add_options(subject_qty_available_units)
        self.view.subject_qty_unit_dropdown.set(subject_qty_unit)

    def process_view_changes(self, *args, **kwargs) -> None:
        def validate_qty(entry: 'gui.SmartEntryWidget') -> None:
            value = entry.get()
            if not value == "":
                try:
                    _ = model.quantity.validation.validate_quantity(float(value))
                    entry.make_valid()
                except (ValueError, model.quantity.exceptions.InvalidQtyError):
                    entry.make_invalid()

        validate_qty(self.view.nutrient_mass_value_entry)
        validate_qty(self.view.subject_qty_value_entry)
        if self.view.nutrient_mass_value_entry.is_valid and self.view.subject_qty_value_entry.is_valid:
            self.view.event_generate("<<Value-Changed>>")


class FixedNutrientRatiosEditorView(tk.LabelFrame):
    """Widget to present a fixed group of nutrient ratio widgets."""

    def __init__(self, **kwargs):
        super().__init__(text="Basic Nutrients", **kwargs)
        self._nutrient_ratio_views: Dict[str, 'NutrientRatioEditorView'] = {}

    def _check_nutrient_not_added(self, nutrient_name: str) -> None:
        """Raise an exception if the nutrient is on board already."""
        if nutrient_name in self._nutrient_ratio_views.keys():
            raise ValueError("Can't add the same nutrient twice")

    def add_nutrient(self, nutrient_ratio_editor_view: 'NutrientRatioEditorView') -> None:
        """Add a nutrient ratio wigit to the group."""
        nutrient_name = nutrient_ratio_editor_view.nutrient_name
        self._check_nutrient_not_added(nutrient_name)
        self._nutrient_ratio_views[nutrient_name] = nutrient_ratio_editor_view
        self._nutrient_ratio_views[nutrient_name].grid(row=len(self._nutrient_ratio_views), column=0, sticky="w")


class DynamicNutrientRatiosEditorView(FixedNutrientRatiosEditorView):
    """Widget to present a changable group of nutrient ratio widgets."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Change the frame label;
        self.configure(text="Extended Nutrients")
        # Add the search button;
        self.add_nutrient_button = tk.Button(master=self, text="Add Nutrient")
        self.add_nutrient_button.grid(row=0, column=0, sticky="w")
        # Install the scroll box;
        self._scrollframe = gui.ScrollFrameWidget(master=self, width=470, height=200)
        self._scrollframe.grid(row=1, column=0, sticky="nsew")

    def add_nutrient(self, nutrient_name: str) -> None:
        """Adds a nutrient ratio widget and remove button to the UI."""
        self._check_nutrient_not_added(nutrient_name)
        widget_frame = tk.Frame(master=self._scrollframe.scrollable_frame)
        self._nutrient_ratio_views[nutrient_name] = NutrientRatioEditorView(
            master=widget_frame,
            nutrient_name=nutrient_name,
            nutrient_display_name=nutrient_name.replace("_", " ")
        )
        self._nutrient_ratio_views[nutrient_name].grid(row=0, column=0)
        remove_button = tk.Button(master=widget_frame, text="Remove")
        remove_button.grid(row=0, column=1)
        widget_frame.pack()


class BasicNutrientRatiosEditorController(gui.HasSubject):
    def __init__(self, view: 'FixedNutrientRatiosEditorView', on_nutrient_values_change_callback: Callable[..., None],
                 **kwargs):
        super().__init__(view=view, subject_type=model.nutrients.HasSettableNutrientRatios, **kwargs)
        self._on_nutrient_values_change_callback = on_nutrient_values_change_callback

        # Dict to store NutrientRatioWidgets;
        self._nutrient_ratio_editor_controllers: Dict[str, 'NutrientRatioEditorController'] = {}

        # Populate the view with a widget for each of the basic (mandatory) nutrients;
        for nutrient_name in model.nutrients.mandatory_nutrient_names:
            # Create the view;
            nutrient_ratio_editor_view = NutrientRatioEditorView(
                master=self.view,
                nutrient_name=nutrient_name,
                nutrient_display_name=nutrient_name.replace("_", " ")
            )
            # Create the controller;
            nutrient_ratio_editor_controller = NutrientRatioEditorController(view=nutrient_ratio_editor_view)
            # Bind the controller to handler;
            nutrient_ratio_editor_view.bind("<<Value-Changed>>", on_nutrient_values_change_callback)
            # Stash the controller and add the widget;
            self._nutrient_ratio_editor_controllers[nutrient_name] = nutrient_ratio_editor_controller
            self.view.add_nutrient(nutrient_ratio_editor_view)

    @property
    def subject(self) -> 'model.nutrients.HasSettableNutrientRatios':
        return super().subject

    def set_subject(self, subject: 'model.nutrients.HasSettableNutrientRatios') -> None:
        super().set_subject(subject)

    @property
    def view(self) -> 'FixedNutrientRatiosEditorView':
        return super().view

    def update_view(self, nutrient_names: Optional[List[str]] = None) -> None:
        # Configure the nutrient ratio's
        for nutr_name, ctrl in self._nutrient_ratio_editor_controllers.items():
            nutr_ratio = self.subject.get_nutrient_ratio(nutr_name)
            ctrl.update_view(
                nutrient_mass_value=nutr_ratio.mass_in_pref_unit_per_subject_g,
                nutrient_mass_unit=nutr_ratio.pref_unit,
                subject_qty_value=self.subject.ref_qty,
                subject_qty_unit=self.subject.pref_unit,
                subject_qty_available_units=self.subject.available_units
            )

    def process_view_changes(self, *args, **kwargs) -> None:
        pass


class DynamicNutrientRatiosEditorController(gui.HasSubject):
    def __init__(self, view: 'DynamicNutrientRatiosEditorView', **kwargs):
        super().__init__(view=view, subject_type=model.nutrients.HasSettableNutrientRatios, **kwargs)

    @property
    def subject(self) -> 'model.nutrients.HasSettableNutrientRatios':
        return super().subject

    def set_subject(self, subject: 'model.nutrients.HasSettableNutrientRatios') -> None:
        super().set_subject(subject)

    @property
    def view(self) -> 'DynamicNutrientRatiosEditorView':
        return super().view

    def update_view(self, *args, **kwargs) -> None:
        pass

    def process_view_changes(self, *args, **kwargs) -> None:
        pass
