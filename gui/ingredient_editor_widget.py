import tkinter as tk
from typing import Optional

import gui
import model


class IngredientEditorWidget(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)

        self.columnconfigure(0, weight=1)  # Make the 0th col expand to fill full width of self.

        # Page title;
        self._title = tk.Label(master=self, text="Ingredient Editor")
        self._title.grid(row=0, column=0)

        # Add the save and reset button to the top;
        self._save_reset_frame = tk.Frame(master=self)
        self.save_button = tk.Button(master=self._save_reset_frame, text="Save")
        self.save_button.bind("<Button-1>", lambda _: self.event_generate("<<save-clicked>>"))
        self.save_button.grid(row=0, column=0, padx=5)
        self.reset_button = tk.Button(master=self._save_reset_frame, text="Reset")
        self.reset_button.bind("<Button-1>", lambda _: self.event_generate("<<reset-clicked>>"))
        self.reset_button.grid(row=0, column=1, padx=5)
        self._save_reset_frame.grid(row=1, column=0, sticky="ew")

        # Basic info groups;
        self._basic_info_frame = tk.Frame(master=self)
        self.name_entry_widget = gui.LabelledEntryWidget(master=self._basic_info_frame,
                                                         label_text="Name",
                                                         entry_width=40,
                                                         invalid_bg=gui.configs.invalid_bg_colour)
        self.name_entry_widget.grid(row=0, column=0, sticky="w")
        self.cost_entry_widget = gui.CostEditorWidget(master=self._basic_info_frame)
        self.cost_entry_widget.grid(row=1, column=0, sticky="w")
        self._basic_info_frame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

    def clear(self) -> None:
        """Clears the fields in the form."""
        self.name_entry_widget.clear()


class IngredientEditorController:

    def __init__(self, app: 'gui.App', view: 'IngredientEditorWidget'):
        self._app = app
        self._view = view
        # Bind the handlers;
        self._view.bind("<<save-clicked>>", self._on_save_clicked)
        self._view.bind("<<reset-clicked>>", self._on_reset_clicked)
        self._view.name_entry_widget.bind("<<Value-Changed>>", self._on_name_changed)
        self._view.cost_entry_widget.bind("<<Cost-Changed>>", self._on_cost_value_changed)
        self._view.cost_entry_widget.bind("<<Qty-Changed>>", self._on_cost_qty_changed)

    @property
    def ingredient_name(self) -> Optional[str]:
        """Gets the value from the ingredient name field."""
        return self._view.name_entry_widget.get()

    def _on_save_clicked(self, event) -> None:
        """Handler for ingredient save."""
        print("save ingredient clicked", self.ingredient_name)

    def _on_reset_clicked(self, event) -> None:
        """Handler for reset button."""
        self._view.clear()

    def _on_name_changed(self, event) -> None:
        """Handler for ingredient name changes."""
        print("name changed!")

    def _on_cost_value_changed(self, _) -> None:
        """Handler for cost value changes."""
        try:
            _ = model.cost.validation.validate_cost(self._view.cost_entry_widget.cost_value)
        except (model.cost.exceptions.CostValueError, ValueError):
            self._view.cost_entry_widget.make_cost_invalid()
            return
        self._view.cost_entry_widget.make_cost_valid()

    def _on_cost_qty_changed(self, event) -> None:
        """Handler for cost qty changes."""
        try:
            _ = model.quantity.validation.validate_quantity(self._view.cost_entry_widget.qty_value)
        except (model.quantity.exceptions.InvalidQtyError, ValueError):
            self._view.cost_entry_widget.make_qty_invalid()
            return
        self._view.cost_entry_widget.make_qty_valid()
