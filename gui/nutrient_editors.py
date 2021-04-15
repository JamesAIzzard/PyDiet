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
    """Handles basic validation, and raises Value-Changed event when the values appear to be valid."""

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

    def add_nutrient_ratio(self, nutrient_ratio_editor_view, **kwargs) -> None:
        """Add a nutrient ratio wigit to the group."""
        nutrient_name = nutrient_ratio_editor_view.nutrient_name
        self._check_nutrient_not_added(nutrient_name)
        self._nutrient_ratio_views[nutrient_name] = nutrient_ratio_editor_view
        self._nutrient_ratio_views[nutrient_name].grid(row=len(self._nutrient_ratio_views), column=0, sticky="w")


class BasicNutrientRatiosEditorController(gui.HasSubject):
    def __init__(self, view: 'FixedNutrientRatiosEditorView', on_nutrient_values_change_callback: Callable[..., None],
                 **kwargs):
        super().__init__(view=view, subject_type=model.nutrients.HasSettableNutrientRatios, **kwargs)
        self._on_nutrient_values_change_callback = on_nutrient_values_change_callback

        # Dict to store NutrientRatioWidgets;
        self._nutrient_ratio_editor_controllers: Dict[str, 'NutrientRatioEditorController'] = {}

        # Populate the view with a widget for each of the basic (mandatory) nutrients;
        self._initialise_nutrient_ratio_editors()

    def _initialise_nutrient_ratio_editors(self) -> None:
        """Add the mandatory nutrients;"""
        for nutrient_name in model.nutrients.mandatory_nutrient_names:
            self.add_nutrient_ratio(nutrient_name)

    def add_nutrient_ratio(self, nutrient_name: str, **kwargs):
        """Adds a nutrient ratio editor."""
        # Validate the nutrient name;
        nutrient_name = model.nutrients.validation.validate_nutrient_name(nutrient_name)
        # Create the view;
        nutrient_ratio_editor_view = NutrientRatioEditorView(
            master=self.view,
            nutrient_name=nutrient_name,
            nutrient_display_name=nutrient_name.replace("_", " ")
        )
        # Create the controller;
        nutrient_ratio_editor_controller = NutrientRatioEditorController(view=nutrient_ratio_editor_view)
        # Bind the controller to handler;
        nutrient_ratio_editor_view.bind("<<Value-Changed>>", self._on_nutrient_values_change_callback)
        # Stash the controller and add the widget;
        self._nutrient_ratio_editor_controllers[nutrient_name] = nutrient_ratio_editor_controller
        self.view.add_nutrient_ratio(nutrient_ratio_editor_view)

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
        self.scrollframe = gui.ScrollFrameWidget(master=self, width=470, height=200)
        self.scrollframe.grid(row=1, column=0, sticky="nsew")
        # Create the new window for the nutrient search
        self._nutrient_search_window = self._nutrient_search_window = tk.Toplevel()
        self._nutrient_search_window.geometry("400x200")
        self._nutrient_search_window.title("Nutrient Search")
        self._nutrient_search_window.protocol("WM_DELETE_WINDOW", self.hide_nutrient_search_window)
        # Create the nutrient search view;
        self.nutrient_search_view = gui.NutrientSearchView(master=self._nutrient_search_window)
        self.nutrient_search_view.pack()
        self.hide_nutrient_search_window()  # Immediately hide;

    def add_nutrient_ratio(self, nutrient_ratio_editor_view, **kwargs) -> None:
        """Adds a nutrient ratio widget and remove button to the UI."""
        nutrient_name = nutrient_ratio_editor_view.nutrient_name
        self._check_nutrient_not_added(nutrient_name)
        self._nutrient_ratio_views[nutrient_name] = nutrient_ratio_editor_view
        self._nutrient_ratio_views[nutrient_name].pack()

    def show_nutrient_search_window(self) -> None:
        """Pop the nutrient search window open."""
        self._nutrient_search_window.deiconify()

    def hide_nutrient_search_window(self) -> None:
        """Hides the nutrient search window."""
        self._nutrient_search_window.withdraw()


class DynamicNutrientRatiosEditorController(BasicNutrientRatiosEditorController):
    def __init__(self, view: 'DynamicNutrientRatiosEditorView', **kwargs):
        super().__init__(view=view, **kwargs)

        self.nutrient_search_controller = gui.NutrientSearchController(
            view=self.view.nutrient_search_view,
            on_result_click=self._on_nutrient_search_result_click
        )

        # Bind the search button to open the new window;
        # Use lambda to avoid passing it an event;
        self.view.add_nutrient_button.bind("<Button-1>", lambda _: self.view.show_nutrient_search_window())

    def _initialise_nutrient_ratio_editors(self) -> None:
        """If there is a subject, populate any extended nutrients."""
        if self.subject is not None:
            for nutrient_name in self.subject.defined_optional_nutrient_ratios:
                self.add_nutrient_ratio(nutrient_name)

    @property
    def subject(self) -> 'model.nutrients.HasSettableNutrientRatios':
        return super().subject

    def set_subject(self, subject: 'model.nutrients.HasSettableNutrientRatios') -> None:
        super().set_subject(subject)

    @property
    def view(self) -> 'DynamicNutrientRatiosEditorView':
        view = super().view
        assert (isinstance(view, DynamicNutrientRatiosEditorView))
        return view

    def add_nutrient_ratio(self, nutrient_name: str, **kwargs):
        """Adds a nutrient ratio editor."""
        # Validate the nutrient name;
        nutrient_name = model.nutrients.validation.validate_nutrient_name(nutrient_name)
        # Create the view;
        editor_frame = tk.Frame(master=self.view.scrollframe.scrollable_frame)
        nutrient_ratio_editor_view = NutrientRatioEditorView(
            master=editor_frame,
            nutrient_name=nutrient_name,
            nutrient_display_name=nutrient_name.replace("_", " ")
        )
        remove_button = tk.Button(master=editor_frame, text="Remove")
        remove_button.bind("<Button-1>", self._on_nutrient_ratio_remove_click)
        nutrient_ratio_editor_view.grid(row=0, column=0)
        remove_button.grid(row=0, column=1)
        # Create the controller;
        nutrient_ratio_editor_controller = NutrientRatioEditorController(view=nutrient_ratio_editor_view)
        # Bind the controller to handler;
        nutrient_ratio_editor_view.bind("<<Value-Changed>>", self._on_nutrient_values_change_callback)
        # Stash the controller and add the widget;
        self._nutrient_ratio_editor_controllers[nutrient_name] = nutrient_ratio_editor_controller
        # self.view.add_nutrient_ratio(editor_frame)

    def _on_nutrient_ratio_remove_click(self, event) -> None:
        print(f"remove {event.widget.nutrient_name}")

    def _on_nutrient_search_result_click(self, event) -> None:
        """Handler for nutrient search result click."""
        self.add_nutrient_ratio(event.widget.nutrient_name)
        self.view.update_idletasks()

    def update_view(self, *args, **kwargs) -> None:
        pass

    def process_view_changes(self, *args, **kwargs) -> None:
        pass