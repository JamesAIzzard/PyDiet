import abc
import tkinter as tk
from typing import List, Dict, Callable, Optional, Union

import gui
import model


class NutrientRatioEditorView(tk.Frame):
    """UI element to display and edit a single nutrient ratio."""

    def __init__(self, nutrient_display_name: str, **kwargs):
        super().__init__(**kwargs)
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
    """Controller for NutrientRatioEditorView.
    - Implements basic validation.
    - Emits Value-Changed event when all values appear to be valid.
    """

    def __init__(self,
                 view: 'NutrientRatioEditorView',
                 nutrient_name: str,
                 on_values_change_callback: Callable[..., None], **kwargs):
        # Validate the nutrient name;
        self._nutrient_name = model.nutrients.validation.validate_nutrient_name(nutrient_name)

        # GO!
        super().__init__(view, **kwargs)
        self._on_values_change_callback = on_values_change_callback
        # Populate the nutrient mass dropdown (these don't change)
        self.view.nutrient_mass_unit_dropdown.add_options(model.quantity.get_recognised_mass_units())
        # Bind change handler;
        self.view.nutrient_mass_value_entry.bind("<<Value-Changed>>", self.process_view_changes)
        self.view.nutrient_mass_unit_dropdown.bind("<<Value-Changed>>", self.process_view_changes)
        self.view.subject_qty_value_entry.bind("<<Value-Changed>>", self.process_view_changes)
        self.view.subject_qty_unit_dropdown.bind("<<Value-Changed>>", self.process_view_changes)

    @property
    def nutrient_name(self) -> str:
        """Returns the nutrient name associated with the editor."""
        return self._nutrient_name

    @property
    def nutrient_mass_value(self) -> Optional[float]:
        """Returns the nutrient mass value."""
        return gui.get_noneable_qty_entry(self.view.nutrient_mass_value_entry)

    @nutrient_mass_value.setter
    def nutrient_mass_value(self, nutrient_mass: Optional[float]) -> None:
        """Sets the nutrient mass value."""
        gui.set_noneable_qty_entry(self.view.nutrient_mass_value_entry, nutrient_mass)

    @property
    def nutrient_mass_unit(self) -> str:
        """Returns the mass unit associated with the nutrient mass value."""
        return self.view.nutrient_mass_unit_dropdown.get()

    @nutrient_mass_unit.setter
    def nutrient_mass_unit(self, mass_unit: str) -> None:
        """Sets the nutrient mass unit dropdown value."""
        self.view.nutrient_mass_unit_dropdown.set(mass_unit)

    @property
    def subject_qty_value(self) -> Optional[float]:
        """Returns the subject quantity value."""
        return gui.get_noneable_qty_entry(self.view.subject_qty_value_entry)

    @subject_qty_value.setter
    def subject_qty_value(self, subject_qty: Optional[float]):
        """Sets the subject quantity value."""
        gui.set_noneable_qty_entry(self.view.subject_qty_value_entry, subject_qty)

    @property
    def subject_qty_unit(self) -> str:
        """Returns the unit associated with the subject value."""
        return self.view.subject_qty_unit_dropdown.get()

    @subject_qty_unit.setter
    def subject_qty_unit(self, qty_unit: str) -> None:
        """Sets the subject quantity unit."""
        self.view.subject_qty_unit_dropdown.set(qty_unit)

    def refresh_subject_qty_units(self, units: List[str]) -> None:
        self.view.subject_qty_unit_dropdown.refresh_options(units)

    @property
    def view(self) -> 'NutrientRatioEditorView':
        return super().view

    def update_view(self, subject: 'model.nutrients.HasNutrientRatios') -> None:
        """Update the view to reflect the argument values."""
        nutrient_ratio = subject.get_nutrient_ratio(self.nutrient_name)
        self.nutrient_mass_value = subject.get_nutrient_mass_in_pref_unit_per_subject_ref_qty(self.nutrient_name)
        self.nutrient_mass_unit = nutrient_ratio.pref_unit
        self.subject_qty_value = subject.ref_qty
        self.refresh_subject_qty_units(subject.available_units)
        self.subject_qty_unit = subject.pref_unit

    def process_view_changes(self, *args, **kwargs) -> None:
        """Run basic validation and raise Value-Changed event if all fields appear to contain
        suitable values."""
        # Validate the fields;
        gui.validate_qty_entry(self.view.nutrient_mass_value_entry)
        gui.validate_qty_entry(self.view.subject_qty_value_entry)
        # If all looks OK, try and fire the callback;
        if self.view.nutrient_mass_value_entry.is_valid and self.view.subject_qty_value_entry.is_valid:
            self._on_values_change_callback(
                nutrient_name=self.nutrient_name,
                nutrient_qty=self.nutrient_mass_value,
                nutrient_qty_unit=self.nutrient_mass_unit,
                subject_qty=self.subject_qty_value,
                subject_qty_unit=self.subject_qty_unit
            )


class FixedNutrientRatiosEditorView(tk.LabelFrame):
    """UI element to present a fixed group of nutrient ratio widgets."""

    def __init__(self, **kwargs):
        super().__init__(text="Basic Nutrients", **kwargs)


class BaseNutrientRatiosEditorController(gui.HasSubject, abc.ABC):
    def __init__(self, view: Union['FixedNutrientRatiosEditorView', 'DynamicNutrientRatiosEditorView'],
                 on_nutrient_values_change_callback: Callable[..., None],
                 **kwargs):
        super().__init__(view=view, subject_type=model.nutrients.HasSettableNutrientRatios, **kwargs)

        # Dict to store NutrientRatioWidgets;
        self.nutrient_ratio_editor_controllers: Dict[str, 'NutrientRatioEditorController'] = {}

        # Stash the change callback;
        self._on_nutrient_values_change_callback = on_nutrient_values_change_callback

    @property
    def subject(self) -> 'model.nutrients.HasSettableNutrientRatios':
        return super().subject

    def set_subject(self, subject: 'model.nutrients.HasSettableNutrientRatios') -> None:
        super().set_subject(subject)

    def update_view(self) -> None:
        """Update the view to reflect the list of nutrient ratios provided."""
        # Go through all the registered editors and make sure they are showing the right things.
        for nutrient_name in self.nutrient_ratio_editor_controllers.keys():
            self.nutrient_ratio_editor_controllers[nutrient_name].update_view(self.subject)

    def process_view_changes(self, *args, **kwargs) -> None:
        pass


class FixedNutrientRatiosEditorController(BaseNutrientRatiosEditorController):
    def __init__(self, view: 'FixedNutrientRatiosEditorView',
                 primary_nutrient_names: List[str],
                 **kwargs):
        super().__init__(view=view, **kwargs)

        # Initialise the fields in the view;
        for nutrient_name in primary_nutrient_names:
            editor_view = NutrientRatioEditorView(master=self.view,
                                                  nutrient_display_name=nutrient_name.replace("_", " "))
            ctrl = NutrientRatioEditorController(
                view=editor_view,
                nutrient_name=nutrient_name,
                on_values_change_callback=self._on_nutrient_values_change_callback
            )
            self.nutrient_ratio_editor_controllers[nutrient_name] = ctrl
            editor_view.grid(row=len(self.nutrient_ratio_editor_controllers), column=1, sticky="w")

    @property
    def view(self) -> 'FixedNutrientRatiosEditorView':
        return super().view


class DynamicNutrientRatiosEditorView(tk.LabelFrame):
    """Widget to present a changable group of nutrient ratio widgets."""

    def __init__(self, **kwargs):
        super().__init__(text="Extended Nutrients", **kwargs)

        # Dict to store editor views;
        self._nutrient_ratio_editor_views: Dict[str, 'NutrientRatioEditorView'] = {}

        # Init the UI elements;
        self.add_nutrient_button = tk.Button(master=self, text="Add Nutrient")
        self._scrollframe = gui.ScrollFrameWidget(master=self, width=470, height=200)
        self._nutrient_search_window = self._nutrient_search_window = tk.Toplevel()
        self._nutrient_search_window.geometry("400x200")
        self._nutrient_search_window.title("Nutrient Search")
        self._nutrient_search_window.protocol("WM_DELETE_WINDOW", self.hide_nutrient_search_window)
        self.nutrient_search_view = gui.NutrientSearchView(master=self._nutrient_search_window)

        # Install the UI;
        self.add_nutrient_button.grid(row=0, column=0, sticky="w")
        self._scrollframe.grid(row=1, column=0, sticky="nsew")
        self.nutrient_search_view.pack()
        self.hide_nutrient_search_window()  # Immediately hide;

    def get_nutrient_ratio_editor(self, nutrient_name: str) -> 'NutrientRatioEditorView':
        """Returns the view element associated with the specified nutrient name."""
        return self._nutrient_ratio_editor_views[nutrient_name]

    def add_nutrient_ratio_editor(self, nutrient_name: str) -> None:
        """Adds a nutrient ratio widget and remove button to the UI."""
        editor_frame = tk.Frame(master=self._scrollframe.scrollable_frame)
        editor = NutrientRatioEditorView(master=editor_frame,
                                         nutrient_display_name=nutrient_name.replace("_", " "))
        self._nutrient_ratio_editor_views[nutrient_name] = editor
        remove_button = tk.Button(master=editor_frame, text="Remove",
                                  command=lambda: editor.event_generate("<<Remove-Clicked>>"))
        editor.grid(row=0, column=0, sticky="w")
        remove_button.grid(row=0, column=1, sticky="w")
        editor_frame.pack()
        self.update_idletasks()

    def remove_nutrient_ratio_editor(self, nutrient_name: str):
        """Removes a nutrient ratio widget"""
        parent_frame = self.get_nutrient_ratio_editor(nutrient_name).master
        parent_frame.pack_forget()
        del self._nutrient_ratio_editor_views[nutrient_name]

    def show_nutrient_search_window(self) -> None:
        """Pop the nutrient search window open."""
        self._nutrient_search_window.deiconify()

    def hide_nutrient_search_window(self) -> None:
        """Hides the nutrient search window."""
        self._nutrient_search_window.withdraw()


class DynamicNutrientRatiosEditorController(BaseNutrientRatiosEditorController):

    def __init__(self, view: 'DynamicNutrientRatiosEditorView', **kwargs):
        super().__init__(view=view, **kwargs)

        # Init controller for search window;
        self._nutrient_search_view_controller = gui.NutrientSearchController(
            view=self.view.nutrient_search_view,
            on_result_click=self._on_nutrient_result_click
        )

        # Bind actions
        self.view.add_nutrient_button.bind("<Button-1>", self._on_add_nutrient_click)

        # Init for any extended nutrients on the subject;
        self.update_view()

    @property
    def view(self) -> 'DynamicNutrientRatiosEditorView':
        return super().view

    def add_nutrient_ratio_editor(self, nutrient_name: str) -> None:
        """Adds a nutrient ratio editor."""
        # Validate the name;
        nutrient_name = model.nutrients.validation.validate_nutrient_name(nutrient_name)

        # Don't add the same nutrient twice;
        if nutrient_name in self.nutrient_ratio_editor_controllers.keys():
            return

        # Init the view;
        self.view.add_nutrient_ratio_editor(nutrient_name)
        self.nutrient_ratio_editor_controllers[nutrient_name] = NutrientRatioEditorController(
            view=self.view.get_nutrient_ratio_editor(nutrient_name),
            nutrient_name=nutrient_name,
            on_values_change_callback=self._on_nutrient_values_change_callback
        )
        # Listen for the remove button click;
        self.nutrient_ratio_editor_controllers[nutrient_name].view.bind("<<Remove-Clicked>>",
                                                                        self._on_remove_nutrient_click)
        # Update the nutreint editor view you jsut added;
        self.nutrient_ratio_editor_controllers[nutrient_name].update_view(self.subject)

    def remove_nutrient_ratio_editor(self, nutrient_name: str) -> None:
        """Removes a nutrient ratio editor."""
        # Validate the name;
        nutrient_name = model.nutrients.validation.validate_nutrient_name(nutrient_name)
        # Wipe the nutrient ratio;
        if self.subject is not None:
            self.subject.undefine_nutrient_ratio(nutrient_name)
        # Drop the view;
        self.view.remove_nutrient_ratio_editor(nutrient_name)
        # Drop the controller;
        del self.nutrient_ratio_editor_controllers[nutrient_name]
        # Push the change to the model;
        self._on_nutrient_values_change_callback(
            nutrient_name=nutrient_name,
            nutrient_qty=None,
            nutrient_qty_unit='g',
            subject_qty=None,
            subject_qty_unit='g'
        )

    def _on_add_nutrient_click(self, _) -> None:
        """Handler for the add nutrient button click."""
        self.view.show_nutrient_search_window()

    def _on_remove_nutrient_click(self, event) -> None:
        """Handler for click on remove nutrient button."""
        # Nasty hack to figure out which nutrient ratio editor had remove pressed.
        # todo: Think of a better way to do this if there is time.
        caller_name = None
        for nutrient_ratio_controller in self.nutrient_ratio_editor_controllers.values():
            if nutrient_ratio_controller.view == event.widget:
                caller_name = nutrient_ratio_controller.nutrient_name
                break
        self.remove_nutrient_ratio_editor(caller_name)

    def _on_nutrient_result_click(self, nutrient_name: str) -> None:
        """Handler for nutrient result click."""
        self.add_nutrient_ratio_editor(nutrient_name)

    def update_view(self) -> None:
        # If there is no view, drop all the editors & return;
        if self.subject is None:
            for nutrient_name in self.nutrient_ratio_editor_controllers.keys():
                self.remove_nutrient_ratio_editor(nutrient_name)
            return

        # Add any nutrient ratios which are defined on the subject, but not in the view yet;
        nutrient_names = []
        for nutrient_name in self.subject.defined_optional_nutrient_ratios:
            if nutrient_name not in self.nutrient_ratio_editor_controllers.keys():
                nutrient_names.append(nutrient_name)
        for nutrient_name in nutrient_names:
            self.add_nutrient_ratio_editor(nutrient_name)
        nutrient_names = []

        # Remove any nutrient ratios which are on the view, but not on the subject;
        for nutrient_name in self.nutrient_ratio_editor_controllers.keys():
            if not self.subject.check_nutrient_ratio_is_defined(nutrient_name):
                nutrient_names.append(nutrient_name)
        for nutrient_name in nutrient_names:
            self.remove_nutrient_ratio_editor(nutrient_name)
        # Now cycle through and update all the views;
        for nutrient_ratio_editor in self.nutrient_ratio_editor_controllers.values():
            nutrient_ratio_editor.update_view(self.subject)
