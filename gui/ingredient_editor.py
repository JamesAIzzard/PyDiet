import tkinter as tk
from typing import Optional

import gui
import model
import persistence


class IngredientEditorView(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)

        self.columnconfigure(0, weight=1)  # Make the 0th col expand to fill full width of self.

        # Add the save and reset button to the top;
        self._save_reset_frame = tk.Frame(master=self)
        self.save_button = tk.Button(master=self._save_reset_frame, text="Save")
        self.save_button.bind("<Button-1>", lambda _: self.event_generate("<<save-clicked>>"))
        self.save_button.grid(row=0, column=0, padx=5)
        self.reset_button = tk.Button(master=self._save_reset_frame, text="Reset")
        self.reset_button.bind("<Button-1>", lambda _: self.event_generate("<<reset-clicked>>"))
        self.reset_button.grid(row=0, column=1, padx=5)
        self._save_reset_frame.grid(row=0, column=0, sticky="ew")

        # Basic info groups;
        self._basic_info_frame = tk.LabelFrame(master=self, text="Basic Info")
        self._name_frame = tk.Frame(master=self._basic_info_frame)
        self._name_entry_label = tk.Label(master=self._name_frame, width=6, text="Name:", anchor="w")
        self._name_entry_label.grid(row=0, column=0, sticky="w")
        self.name_entry = gui.SmartEntryWidget(master=self._name_frame, width=30,
                                               invalid_bg=gui.configs.invalid_bg_colour)
        self.name_entry.bind("<<Value-Changed>>", lambda _: self.name_entry.event_generate("<<View-Change>>"))
        self.name_entry.grid(row=0, column=1)
        self._name_frame.grid(row=0, column=0, sticky="w")
        self.cost_editor = gui.CostEditorView(master=self._basic_info_frame)
        self.cost_editor.grid(row=1, column=0)
        self._basic_info_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        # Bulk editor;
        self.bulk_editor = gui.BulkEditorView(master=self)
        self.bulk_editor.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        # Nutrient-Flag Status Widget;
        self.nutrient_flag_status_widget = gui.FlagNutrientStatusView(master=self)
        self.nutrient_flag_status_widget.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        # Flag editor;
        self.flag_editor = gui.FlagEditorView(master=self)
        self.flag_editor.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

        # Mandatory nutrient editor;
        self.basic_nutrient_ratios_editor = gui.FixedNutrientRatiosEditorView(master=self)
        self.basic_nutrient_ratios_editor.grid(row=5, column=0, padx=5, pady=5, sticky="ew")

        # Dynamic nutrient editor;
        self.extended_nutrient_ratios_editor = gui.DynamicNutrientRatiosEditorView(master=self)
        self.extended_nutrient_ratios_editor.grid(row=6, column=0, padx=5, pady=5, sticky="ew")

    def clear(self) -> None:
        """Clears the fields in the form."""
        self.name_entry.clear()


class IngredientNameEntryController(gui.HasSubject):
    def __init__(self, view: 'gui.SmartEntryWidget', **kwargs):
        super().__init__(view=view, subject_type=model.ingredients.Ingredient, **kwargs)
        self.view.bind("<<Value-Changed>>", self.process_view_changes)

    @property
    def view(self) -> 'gui.SmartEntryWidget':
        view = super().view
        assert (isinstance(view, gui.SmartEntryWidget))
        return view

    @property
    def subject(self) -> 'model.ingredients.Ingredient':
        return super().subject

    def set_subject(self, subject: 'model.ingredients.Ingredient') -> None:
        super().set_subject(subject)

    def update_view(self) -> None:
        if self.subject is None:
            return
        if self.subject.name_is_defined:
            self.view.set(self.subject.name)

    def process_view_changes(self, _) -> None:
        value = self.view.get()
        if value == "":
            self.subject.name = None
        else:
            if persistence.check_unique_value_available(
                    cls=model.ingredients.Ingredient,
                    proposed_name=value,
                    ignore_datafile=self.subject.datafile_name
            ):
                self.subject.name = value
                self.view.make_valid()
            else:
                self.view.make_invalid()


class IngredientEditorController(gui.HasSubject):
    def __init__(self, view: 'IngredientEditorView', **kwargs):
        super().__init__(subject_type=model.ingredients.Ingredient, view=view, **kwargs)

        # Child controllers;
        self.name_entry = IngredientNameEntryController(view=view.name_entry, **kwargs)
        self.cost_editor = gui.CostEditorController(view=view.cost_editor, **kwargs)
        self.bulk_editor = gui.BulkEditorController(view=view.bulk_editor, **kwargs)
        self.nutrient_flag_status = gui.FlagNutrientStatusController(
            view=view.nutrient_flag_status_widget,
            **kwargs
        )
        self.flag_editor = gui.FlagEditorController(
            view=view.flag_editor,
            on_flag_value_change_callback=self._on_flag_value_changed,
            **kwargs
        )
        self.basic_nutrient_ratio_editor = gui.FixedNutrientRatiosEditorController(
            view=view.basic_nutrient_ratios_editor,
            on_nutrient_values_change_callback=self._on_nutrient_values_changed,
            primary_nutrient_names=model.nutrients.mandatory_nutrient_names,
            **kwargs
        )
        self.extended_nutrient_ratio_editor = gui.DynamicNutrientRatiosEditorController(
            view=view.extended_nutrient_ratios_editor,
            on_nutrient_values_change_callback=self._on_nutrient_values_changed,
            **kwargs
        )

        # Markers to stop circular updates between nutrients and flags;
        self.editing_nutrients: bool = False
        self.editing_flags: bool = False

        # Bind handlers;
        self.view.bind("<<save-clicked>>", self._on_save_clicked)
        self.view.bind("<<reset-clicked>>", self._on_reset_clicked)

        # Stick a message in the nutrient flag status;
        self.nutrient_flag_status.update_view("No conflicts.")

    @property
    def subject(self) -> 'model.ingredients.Ingredient':
        return super().subject

    def set_subject(self, subject: 'model.ingredients.Ingredient') -> None:
        self.name_entry.set_subject(subject)
        self.cost_editor.set_subject(subject)
        self.bulk_editor.set_subject(subject)
        self.flag_editor.set_subject(subject)
        self.basic_nutrient_ratio_editor.set_subject(subject)
        self.extended_nutrient_ratio_editor.set_subject(subject)
        super().set_subject(subject)

    def update_view(self) -> None:
        pass

    def process_view_changes(self, _) -> None:
        pass

    @property
    def view(self) -> 'gui.IngredientEditorView':
        view = super().view
        assert (isinstance(view, gui.IngredientEditorView))
        return view

    def _on_save_clicked(self, _) -> None:
        """Handler for ingredient save."""
        print("save pressed")

    def _on_reset_clicked(self, _) -> None:
        """Handler for reset button."""
        self.view.clear()

    def _on_nutrient_values_changed(self,
                                    nutrient_name: str,
                                    nutrient_qty: Optional[float] = None,
                                    nutrient_qty_unit: str = 'g',
                                    subject_qty: Optional[float] = None,
                                    subject_qty_unit: str = 'g'
                                    ) -> None:
        """Handler for changes to nutrient values."""
        # Catch unset subject;
        if self.subject is None:
            return

        # Determine the type of update;
        if self.editing_nutrients is False and self.editing_flags is False:
            self.editing_nutrients = True

        try:
            print(f"setting {nutrient_name}")
            self.subject.set_nutrient_ratio(
                nutrient_name=nutrient_name,
                nutrient_qty=nutrient_qty,
                nutrient_qty_unit=nutrient_qty_unit,
                subject_qty=subject_qty,
                subject_qty_unit=subject_qty_unit
            )
        except model.nutrients.exceptions.ChildNutrientQtyExceedsParentNutrientQtyError:
            self.nutrient_flag_status.update_view(
                f"{nutrient_name.replace('_', ' ')} qty exceeds its parent group."
            )
            # Reset the update state;
            self.editing_nutrients = False
            return

        # Update the right views;
        if self.editing_nutrients:
            print("updating flag views")
            self.flag_editor.update_view()

        # Reset the update state;
        self.editing_nutrients = False

        # Reset the conflict message;
        self.nutrient_flag_status.update_view("No conflicts.")

    def _on_flag_value_changed(self, event) -> None:
        """Handler for changes to flag values."""
        # Catch unset subject;
        if self.subject is None:
            return

        # Determine which part of the UI is being editied to prevent circular update dependency.
        if self.editing_nutrients is False and self.editing_flags is False:
            self.editing_flags = True

        # Try and move the flag values into the model;
        try:
            for flag_name, flag_value in self.flag_editor.flag_values.items():
                self.subject.set_flag_value(flag_name, self.view.flag_editor.get_flag_value(flag_name), True)
                print(f"setting {flag_name}")
        except (model.flags.exceptions.NonZeroNutrientRatioConflictError,
                model.flags.exceptions.UndefineMultipleNutrientRatiosError) as e:
            self.nutrient_flag_status.update_view(
                f"'{flag_name.replace('_', ' ')}' flag conflicts with {e.conflicting_nutrient_ratios[0].nutrient.primary_name} nutrient ratio"
            )
            # Reset the circular dependency flag;
            self.editing_flags = False
            return

        # Update the views;
        if self.editing_flags:
            print("updating nutrient views")
            self.basic_nutrient_ratio_editor.update_view()
            self.extended_nutrient_ratio_editor.update_view()

        # Reset the circular dependency flag;
        self.editing_flags = False

        # Reset the conflict message;
        self.nutrient_flag_status.update_view("No conflicts.")
