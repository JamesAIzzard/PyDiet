import tkinter as tk

import gui
import model
import persistence


class IngredientEditorWidget(tk.Frame):
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
        self._name_entry_label = tk.Label(master=self._name_frame, text="Name:")
        self._name_entry_label.grid(row=0, column=0, sticky="w")
        self.name_entry = gui.SmartEntryWidget(master=self._name_frame, width=30,
                                               invalid_bg=gui.configs.invalid_bg_colour)
        self.name_entry.grid(row=0, column=1)
        self._name_frame.grid(row=0, column=0, sticky="w")
        self.cost_editor = gui.CostEditorWidget(master=self._basic_info_frame)
        self.cost_editor.grid(row=1, column=0)
        self._basic_info_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        # Bulk editor;
        self.bulk_info_editor = gui.BulkEditorWidget(master=self)
        self.bulk_info_editor.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        # Flag editor;
        self.flag_editor = gui.FlagEditorWidget(master=self)
        self.flag_editor.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        # # Mandatory nutrient editor;
        # self.mandatory_nutrient_editor = gui.FixedNutrientEditor(master=self)
        # self.mandatory_nutrient_editor.grid(row=4, column=0, padx=5, pady=5)
        #
        # # Dynamic nutrient editor;
        # self.dynamic_nutrient_editor = gui.DynamicNutrientEditor(master=self)
        # self.dynamic_nutrient_editor.grid(row=5, column=0, padx=5, pady=5)

    def clear(self) -> None:
        """Clears the fields in the form."""
        self.name_entry.clear()


class HasIngredientNameWidget(gui.HasSubject):
    def __init__(self, ingredient_name_editor_widget: 'gui.SmartEntryWidget',
                 **kwargs):
        super().__init__(**kwargs)
        self._ingredient_name_editor_widget = ingredient_name_editor_widget
        # Bind handlers to widget events;
        self._ingredient_name_editor_widget.bind("<<Value-Changed>>", self._on_ingredient_name_change)

    @property
    def ingredient_name(self) -> str:
        """Returns the value from the ingredient name entry."""
        return self._ingredient_name_editor_widget.get()

    @ingredient_name.setter
    def ingredient_name(self, ingredient_name: str) -> None:
        """Sets the value from the ingredient name entry."""
        self._ingredient_name_editor_widget.set(ingredient_name)

    def _on_ingredient_name_change(self, _) -> None:
        """Handler for changes to the ingredient name."""
        # Check the name value is allowed;
        if not persistence.check_unique_value_available(
                cls=model.ingredients.Ingredient,
                proposed_name=self._ingredient_name_editor_widget.get(),
                ignore_datafile=self.subject.datafile_name
        ):
            self._ingredient_name_editor_widget.make_invalid()
        else:
            subject: 'model.ingredients.Ingredient' = self.subject
            self._ingredient_name_editor_widget.make_valid()
            subject.name = self._ingredient_name_editor_widget.get()


class IngredientEditorController(HasIngredientNameWidget, gui.HasCostEditorWidget, gui.HasFlagEditorWidget):

    def __init__(self, ingredient_editor_widget: 'IngredientEditorWidget', **kwargs):
        super().__init__(
            subject_type=model.ingredients.Ingredient,
            ingredient_name_editor_widget=ingredient_editor_widget.name_entry,
            cost_editor_widget=ingredient_editor_widget.cost_editor,
            flag_editor_widget=ingredient_editor_widget.flag_editor,
            **kwargs
        )
        self._ingredient_editor_widget = ingredient_editor_widget

        # Bind handlers;
        self._ingredient_editor_widget.bind("<<save-clicked>>", self._on_save_clicked)
        self._ingredient_editor_widget.bind("<<reset-clicked>>", self._on_reset_clicked)

    def _on_save_clicked(self, _) -> None:
        """Handler for ingredient save."""
        print("save ingredient clicked", self.subject)

    def _on_reset_clicked(self, _) -> None:
        """Handler for reset button."""
        self._ingredient_editor_widget.clear()
