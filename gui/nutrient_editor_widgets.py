import tkinter as tk
from typing import Dict

import gui
import model


class NutrientRatioEditorWidget(tk.Frame):
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


class FixedNutrientRatiosEditorWidget(tk.LabelFrame):
    """Class to define common functionality across nutrient ratio editors."""

    def __init__(self, **kwargs):
        super().__init__(text="Basic Nutrients", **kwargs)
        self.nutrient_ratio_widgets: Dict[str, 'NutrientRatioEditorWidget'] = {}

    def _check_nutrient_not_added(self, nutrient_name: str) -> None:
        """Raise an exception if the nutrient is on board already."""
        if nutrient_name in self.nutrient_ratio_widgets.keys():
            raise ValueError("Can't add the same nutrient twice")

    def add_nutrient_ratio_widget(self, nutrient_name: str) -> None:
        """Add a nutrient ratio wigit to the group."""
        self._check_nutrient_not_added(nutrient_name)
        self.nutrient_ratio_widgets[nutrient_name] = NutrientRatioEditorWidget(
            master=self,
            nutrient_name=nutrient_name,
            nutrient_display_name=nutrient_name.replace("_", " ")
        )
        self.nutrient_ratio_widgets[nutrient_name].grid(row=len(self.nutrient_ratio_widgets), column=0, sticky="w")


class DynamicNutrientRatiosEditorWidget(FixedNutrientRatiosEditorWidget):
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
        self.nutrient_ratio_widgets[nutrient_name] = NutrientRatioEditorWidget(
            master=widget_frame,
            nutrient_name=nutrient_name,
            nutrient_display_name=nutrient_name.replace("_", " ")
        )
        self.nutrient_ratio_widgets[nutrient_name].grid(row=0, column=0)
        remove_button = tk.Button(master=widget_frame, text="Remove")
        remove_button.grid(row=0, column=1)
        widget_frame.pack()


def check_settable_nutrient_ratios(controller: 'gui.HasSubject') -> None:
    # Check the subject has editable nutrient ratios;
    if not issubclass(controller._subject_type, model.nutrients.HasSettableNutrientRatios):
        raise TypeError("FixedNutrientRatiosEditorWidget requires the subject to support settable nutrient ratios.")


class HasFixedNutrientRatiosEditorWidget(gui.HasSubject):
    def __init__(self, fixed_nutrient_ratios_editor_widget: 'FixedNutrientRatiosEditorWidget', **kwargs):
        super().__init__(**kwargs)

        # Check the subject has editable nutrient ratios;
        check_settable_nutrient_ratios(self)

        # Stash a reference to the view;
        self._fixed_nutrient_ratios_editor_widget = fixed_nutrient_ratios_editor_widget

        # Init the mandatory nutrients;
        for nutrient_name in model.nutrients.mandatory_nutrient_names:
            self._fixed_nutrient_ratios_editor_widget.add_nutrient_ratio_widget(nutrient_name)

    def _set_subject(self, subject: 'model.nutrients.HasSettableNutrientRatios') -> None:
        super()._set_subject(subject)


class HasDynamicNutrientRatiosEditorWidget(gui.HasSubject):
    def __init__(self, dynamic_nutrient_ratios_editor_widget: 'DynamicNutrientRatiosEditorWidget', **kwargs):
        super().__init__(**kwargs)

        # Check the subject has editable nutrient ratios;
        check_settable_nutrient_ratios(self)

        # Stash a reference to the view;
        self._dynamic_nutrient_ratios_editor_widget = dynamic_nutrient_ratios_editor_widget

        # Init the mandatory nutrients;
        for nutrient_name in model.nutrients.all_primary_nutrient_names:
            self._dynamic_nutrient_ratios_editor_widget.add_nutrient_ratio_widget(nutrient_name)

    def _set_subject(self, subject: 'model.nutrients.HasSettableNutrientRatios') -> None:
        super()._set_subject(subject)
