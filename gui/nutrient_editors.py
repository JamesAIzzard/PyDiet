import tkinter as tk
from typing import List, Dict, Optional, Any

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


class FixedNutrientRatiosEditorView(tk.LabelFrame):
    """Widget to present a fixed group of nutrient ratio widgets."""

    def __init__(self, **kwargs):
        super().__init__(text="Basic Nutrients", **kwargs)
        self.nutrient_ratio_widgets: Dict[str, 'NutrientRatioEditorView'] = {}

    def _check_nutrient_not_added(self, nutrient_name: str) -> None:
        """Raise an exception if the nutrient is on board already."""
        if nutrient_name in self.nutrient_ratio_widgets.keys():
            raise ValueError("Can't add the same nutrient twice")

    def add_nutrient_ratio_widget(self, nutrient_name: str) -> None:
        """Add a nutrient ratio wigit to the group."""
        self._check_nutrient_not_added(nutrient_name)
        self.nutrient_ratio_widgets[nutrient_name] = NutrientRatioEditorView(
            master=self,
            nutrient_name=nutrient_name,
            nutrient_display_name=nutrient_name.replace("_", " ")
        )
        self.nutrient_ratio_widgets[nutrient_name].grid(row=len(self.nutrient_ratio_widgets), column=0, sticky="w")


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

    def add_nutrient_ratio_widget(self, nutrient_name: str) -> None:
        """Adds a nutrient ratio widget and remove button to the UI."""
        self._check_nutrient_not_added(nutrient_name)
        widget_frame = tk.Frame(master=self._scrollframe.scrollable_frame)
        self.nutrient_ratio_widgets[nutrient_name] = NutrientRatioEditorView(
            master=widget_frame,
            nutrient_name=nutrient_name,
            nutrient_display_name=nutrient_name.replace("_", " ")
        )
        self.nutrient_ratio_widgets[nutrient_name].grid(row=0, column=0)
        remove_button = tk.Button(master=widget_frame, text="Remove")
        remove_button.grid(row=0, column=1)
        widget_frame.pack()


class BasicNutrientRatiosEditorController(gui.HasSubject):
    def __init__(self, view: 'FixedNutrientRatiosEditorView', **kwargs):
        super().__init__(view=view, subject_type=model.nutrients.HasSettableNutrientRatios, **kwargs)
        # Populate the view with a widget for each of the basic (mandatory) nutrients;
        for nutrient_name in model.nutrients.mandatory_nutrient_names:
            self.view.add_nutrient_ratio_widget(nutrient_name)

    @property
    def subject(self) -> 'model.nutrients.HasSettableNutrientRatios':
        return super().subject

    def set_subject(self, subject: 'model.nutrients.HasSettableNutrientRatios') -> None:
        super().set_subject(subject)

    @property
    def view(self) -> 'FixedNutrientRatiosEditorView':
        return super().view

    def _update_nutrient_names(self, nutrient_names: Optional[List[str]] = None) -> None:
        """Update the listed nutrient names on the widget."""
        # Check they are all in the widget before doing anything else;
        for nutrient_name in nutrient_names:
            if nutrient_name not in self.view.nutrient_ratio_widgets.keys():
                raise ValueError(f"{nutrient_name} is not a nutrient in the view.")
        # Update the view for each nutrient listed;
        for nutrient_name in nutrient_names:
            # Grab the widget in question;
            nutrient_editor_view = self.view.nutrient_ratio_widgets[nutrient_name]
            # Set the subject qty value;
            nutrient_editor_view.subject_qty_value_entry.set(str(self.subject.ref_qty))
            # Set the subject qty unit;
            nutrient_editor_view.subject_qty_unit_dropdown.set(str(self.subject.pref_unit))
            # If the nutrient isn't defined, just skip the rest;
            if not self.subject.check_nutrient_ratio_is_defined(nutrient_name):
                continue
            # Grab the nutrient ratio instance;
            nutrient_ratio = self.subject.get_nutrient_ratio(nutrient_name)
            # Set the mass value entry;
            mass_value: float = self.subject.get_nutrient_mass_in_pref_unit_per_subject_ref_qty(nutrient_name)
            nutrient_editor_view.nutrient_mass_value_entry.set(str(mass_value))
            # Set the nutrient unit dropdown;
            nutrient_editor_view.nutrient_mass_unit_dropdown.set(nutrient_ratio.pref_unit)

    def update_view(self, nutrient_names: Optional[List[str]] = None) -> None:
        # Configure all the unit dropdowns based on the subject's bulk configuration;
        for nutrient_editor_view in self.view.nutrient_ratio_widgets.values():
            nutrient_editor_view.nutrient_mass_unit_dropdown.remove_options()
            nutrient_editor_view.subject_qty_unit_dropdown.remove_options()
            nutrient_editor_view.nutrient_mass_unit_dropdown.add_options(model.quantity.get_recognised_mass_units())
            nutrient_editor_view.subject_qty_unit_dropdown.add_options(model.quantity.get_recognised_mass_units())
            if self.subject.density_is_defined:
                nutrient_editor_view.subject_qty_unit_dropdown.add_options(model.quantity.get_recognised_vol_units())
            if self.subject.piece_mass_defined:
                nutrient_editor_view.subject_qty_unit_dropdown.add_options(model.quantity.get_recognised_pc_units())
        # If particular nutrient names were not passed, populate with all mandatory nutrient names;
        if nutrient_names is None:
            nutrient_names = model.nutrients.mandatory_nutrient_names
        self._update_nutrient_names(nutrient_names)

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
