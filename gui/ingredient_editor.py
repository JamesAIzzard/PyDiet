import tkinter as tk
from tkinter import messagebox
from typing import Optional

import gui
import model
import persistence


class IngredientEditorView(tk.Frame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.columnconfigure(0, weight=1)  # Make the 0th col expand to fill full width of self.

        # Add the save and reset button to the top;
        self._save_reset_frame = tk.Frame(master=self)
        self.save_button = tk.Button(master=self._save_reset_frame, text="Save")
        self.save_button.bind("<Button-1>", lambda _: self.event_generate("<<save-clicked>>"))
        self.save_button.grid(row=0, column=0, padx=5)
        self.reset_button = tk.Button(master=self._save_reset_frame, text="Reset")
        self._save_reset_frame.grid(row=0, column=0, sticky="ew")

        # Basic info groups;
        self._basic_info_frame = tk.LabelFrame(master=self, text="Basic Info")
        self._name_frame = tk.Frame(master=self._basic_info_frame)
        self._name_entry_label = tk.Label(master=self._name_frame, width=6, text="Name:", anchor="w")
        self._name_entry_label.grid(row=0, column=0, sticky="w")
        self.name_entry = gui.SmartEntryWidget(master=self._name_frame, width=50,
                                               invalid_bg=gui.configs.invalid_bg_colour)
        self.name_entry.bind("<<Value-Changed>>", lambda _: self.name_entry.event_generate("<<View-Change>>"))
        self.name_entry.grid(row=0, column=1)
        self._name_frame.grid(row=0, column=0, sticky="w")
        self.cost_editor = gui.CostEditorView(master=self._basic_info_frame)
        self.cost_editor.grid(row=1, column=0, sticky="w")
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


class IngredientNameEntryController(gui.HasSubject, gui.SupportsValidity, gui.SupportsDefinition):
    def __init__(self, view: 'gui.SmartEntryWidget', **kwargs):
        super().__init__(view=view, subject_type=model.ingredients.ReadonlyIngredient, **kwargs)
        self.view.bind("<<Value-Changed>>", self.process_view_changes)

    @property
    def name(self) -> Optional[str]:
        """Gets the ingredient name."""
        if self.view.get().replace(" ", "") == "":
            return None
        else:
            return self.view.get().strip()

    @name.setter
    def name(self, name: Optional[str]) -> None:
        """Sets the ingredient name."""
        if name is None:
            name = ""
        self.view.set(name.strip())

    @property
    def is_valid(self) -> bool:
        return self.view.is_valid

    @property
    def is_defined(self) -> bool:
        return self.name is not None

    @property
    def view(self) -> 'gui.SmartEntryWidget':
        view = super().view
        assert (isinstance(view, gui.SmartEntryWidget))
        return view

    @property
    def subject(self) -> 'model.ingredients.ReadonlyIngredient':
        return super().subject

    def set_subject(self, subject: 'model.ingredients.ReadonlyIngredient') -> None:
        super().set_subject(subject)

    def update_view(self) -> None:
        if self.subject is None:
            return
        if self.subject.name_is_defined:
            self.name = self.subject.name
        else:
            self.name = None

    def process_view_changes(self, _) -> None:
        value = self.view.get()
        if value == "":
            self.subject.name = None
        else:
            if persistence.check_unique_value_available(
                    cls=model.ingredients.ReadonlyIngredient,
                    proposed_value=value,
                    ignore_datafile=self.subject.datafile_name
            ):
                self.subject.name = value
                self.view.make_valid()
            else:
                self.view.make_invalid()


class IngredientEditorController(gui.HasSubject):
    def __init__(self, view: 'IngredientEditorView', **kwargs):
        super().__init__(subject_type=model.ingredients.ReadonlyIngredient, view=view, **kwargs)

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
            primary_nutrient_names=model.nutrients.MANDATORY_NUTRIENT_NAMES,
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
        self.bulk_editor.ref_qty_editor.view.bind("<<Ref-Qty-Changed>>", self._on_bulk_properties_changed)
        self.bulk_editor.density_editor.view.bind("<<Density-Changed>>", self._on_bulk_properties_changed)
        self.bulk_editor.piece_mass_editor.view.bind("<<Piece-Mass-Changed>>", self._on_bulk_properties_changed)
        self.view.bind("<<save-clicked>>", self._on_save_clicked)

        # Stick a message in the nutrient flag status;
        self.nutrient_flag_status.show_ok()

    @property
    def subject(self) -> 'model.ingredients.ReadonlyIngredient':
        return super().subject

    def set_subject(self, subject: 'model.ingredients.ReadonlyIngredient') -> None:
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

    def _on_save_clicked(self, _) -> bool:
        """Handler for ingredient save."""

        def show_save_message(message: str) -> None:
            messagebox.showinfo(title="PyDiet", message=message)

        # Work through the fields, checking they are valid.
        # First check the name is populated and valid;
        if self.name_entry.is_undefined:
            show_save_message("Ingredient name is required.")
            return False
        if self.name_entry.is_invalid:
            show_save_message("Ingredient name must be unique.")
            return False

        # Now check through cost;
        if self.cost_editor.is_undefined:
            show_save_message("Cost field must be completed.")
            return False
        if self.cost_editor.is_invalid:
            show_save_message("Cost field must be valid.")
            return False

        # Now check ref qty;
        if self.bulk_editor.ref_qty_editor.is_undefined:
            show_save_message("Reference quantity field must be completed.")
            return False
        if self.bulk_editor.ref_qty_editor.is_invalid:
            show_save_message("Reference quantity field must be valid.")
            return False

        # Now check density;
        if self.bulk_editor.density_editor.is_invalid:
            show_save_message("Density field must be valid or empty.")
            return False

        # Now check piece mass;
        if self.bulk_editor.piece_mass_editor.is_invalid:
            show_save_message("Piece mass field must be valid or empty.")
            return False

        # Now check flag nutrient relations;
        if self.nutrient_flag_status.has_conflict:
            show_save_message("Nutrient-flag conflicts must be resolved before saving.")
            return False

        for nutrient_name in self.basic_nutrient_ratio_editor.nutrient_names:
            nutrient_editor = self.basic_nutrient_ratio_editor.get_nutrient_ratio_editor(nutrient_name)
            if nutrient_editor.is_invalid:
                show_save_message(f"{nutrient_name.replace('_', ' ')} must be valid before saving.")
                return False
            if nutrient_editor.is_undefined:
                show_save_message(f"{nutrient_name.replace('_', ' ')} must be defined before saving.")
                return False

        for nutrient_name in self.extended_nutrient_ratio_editor.nutrient_names:
            nutrient_editor = self.extended_nutrient_ratio_editor.get_nutrient_ratio_editor(nutrient_name)
            if nutrient_editor.is_invalid:
                show_save_message(f"{nutrient_name.replace('_', ' ')} cannot be invalid.")
                return False

        # All OK, go ahead and save;
        persistence.save_instance(self.subject)
        gui.app.root.title("Ingredient Editor")
        show_save_message(f"{self.subject.name} saved!")
        return True

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
            for ntr_name in self.basic_nutrient_ratio_editor.nutrient_names:
                ntr_editor = self.basic_nutrient_ratio_editor.get_nutrient_ratio_editor(ntr_name)
                self.subject.set_nutrient_ratio(
                    nutrient_name=ntr_editor.nutrient_name,
                    nutrient_qty=ntr_editor.nutrient_mass_value,
                    nutrient_qty_unit=ntr_editor.nutrient_mass_unit,
                    subject_qty=ntr_editor.subject_qty_value,
                    subject_qty_unit=ntr_editor.subject_qty_unit
                )
                self.subject.set_nutrient_pref_unit(nutrient_name, nutrient_qty_unit)
            for ntr_name in self.extended_nutrient_ratio_editor.nutrient_names:
                ntr_editor = self.extended_nutrient_ratio_editor.get_nutrient_ratio_editor(ntr_name)
                self.subject.set_nutrient_ratio(
                    nutrient_name=ntr_editor.nutrient_name,
                    nutrient_qty=ntr_editor.nutrient_mass_value,
                    nutrient_qty_unit=ntr_editor.nutrient_mass_unit,
                    subject_qty=ntr_editor.subject_qty_value,
                    subject_qty_unit=ntr_editor.subject_qty_unit
                )
                self.subject.set_nutrient_pref_unit(nutrient_name, nutrient_qty_unit)
            # Update the right views;
            if self.editing_nutrients:
                self.flag_editor.update_view()

            # Reset the update state;
            self.editing_nutrients = False

            # Reset the conflict message;
            self.nutrient_flag_status.show_ok()
        except model.nutrients.exceptions.NutrientFamilyRatioConflictError as err:
            self.nutrient_flag_status.show_conflict(
                f"The nutrients in the {err.nutrient_group_name} group exceed its mass."
            )
        except model.nutrients.exceptions.NutrientMassExceedsSubjectQtyError as err:
            self.nutrient_flag_status.show_conflict(
                f"The mass of {err.nutrient_name} exceeds its stated ingredient mass."
            )
        finally:
            self.editing_nutrients = False
            # Update the right views;
            if self.editing_nutrients:
                self.flag_editor.update_view()

    def _on_flag_value_changed(self, event) -> None:
        """Handler for changes to flag values."""
        # Catch unset subject;
        if self.subject is None:
            return

        # Determine which part of the UI is being editied to prevent circular update dependency.
        if self.editing_nutrients is False and self.editing_flags is False:
            self.editing_flags = True

        # Try and move the flag values into the model;
        flag_name = None
        try:
            for flag_name, flag_value in self.flag_editor.flag_values.items():
                self.subject.set_flag_value(flag_name, self.view.flag_editor.get_flag_value(flag_name), True)
        except (model.exceptions.NonZeroNutrientRatioConflictError,
                model.exceptions.MultipleUndefinedRelatedNutrientRatiosError) as e:
            self.nutrient_flag_status.show_conflict(
                f"'{flag_name.replace('_', ' ')}' flag conflicts with {e.conflicting_nutrient_ratios[0].nutrient.primary_name} nutrient ratio"
                # noqa
            )
            # Reset the circular dependency flag;
            self.editing_flags = False
            return

        # Update the views;
        if self.editing_flags:
            self.basic_nutrient_ratio_editor.update_view()
            self.extended_nutrient_ratio_editor.update_view()

        # Reset the circular dependency flag;
        self.editing_flags = False

        # Reset the conflict message;
        self.nutrient_flag_status.show_ok()

    def _on_bulk_properties_changed(self, event) -> None:
        """Handler for bulk properties changing."""

        # Catch empty subject;
        if self.subject is None:
            return

        self.cost_editor.update_view()
        self.bulk_editor.update_view()
        self.basic_nutrient_ratio_editor.update_view()
        self.extended_nutrient_ratio_editor.update_view()
