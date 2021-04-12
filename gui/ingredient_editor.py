import tkinter as tk

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

        # Flag editor;
        self.flag_editor = gui.FlagEditorWidget(master=self)
        self.flag_editor.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        # Mandatory nutrient editor;
        self.basic_nutrient_ratios_editor = gui.FixedNutrientRatiosEditorWidget(master=self)
        self.basic_nutrient_ratios_editor.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

        # Dynamic nutrient editor;
        self.extended_nutrient_ratios_editor = gui.DynamicNutrientRatiosEditorWidget(master=self)
        self.extended_nutrient_ratios_editor.grid(row=5, column=0, padx=5, pady=5, sticky="ew")

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
        self.name_entry_controller = IngredientNameEntryController(view=view.name_entry, **kwargs)
        self.cost_editor_controller = gui.CostEditorController(view=view.cost_editor, **kwargs)
        self.bulk_editor_controller = gui.BulkEditorController(view=view.bulk_editor, **kwargs)

        # Bind handlers;
        self.view.bind("<<save-clicked>>", self._on_save_clicked)
        self.view.bind("<<reset-clicked>>", self._on_reset_clicked)

    @property
    def subject(self) -> 'model.ingredients.Ingredient':
        return super().subject

    def set_subject(self, subject: 'model.ingredients.Ingredient') -> None:
        self.name_entry_controller.set_subject(subject)
        self.cost_editor_controller.set_subject(subject)
        self.bulk_editor_controller.set_subject(subject)
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
        print("save ingredient clicked", self.subject)

    def _on_reset_clicked(self, _) -> None:
        """Handler for reset button."""
        self.view.clear()
