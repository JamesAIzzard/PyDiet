import tkinter as tk
from typing import List, Dict, Optional

import gui
import model.ingredients
import persistence


class IngredientSearchResultWidget(tk.Frame):
    def __init__(self, ingredient_name: str, **kwargs):
        super().__init__(**kwargs)
        self.ingredient_name = ingredient_name
        self._ingredient_name_label = tk.Label(master=self, text=ingredient_name, width=60, background="#c0c0c0",
                                               anchor="w")
        self.edit_button = tk.Button(master=self, text="Edit")
        self.delete_button = tk.Button(master=self, text="Delete")
        self._ingredient_name_label.grid(row=0, column=0, sticky="ew")
        self.edit_button.grid(row=0, column=1, sticky="ew")


class IngredientSearchWidget(tk.Frame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Init the search bar;
        self.search_frame = tk.Frame(master=self)
        self.search_entry = gui.SmartEntryWidget(master=self.search_frame, width=50)
        self.search_button = tk.Button(master=self.search_frame, text="Search")
        self.search_entry.grid(row=0, column=0)
        self.search_button.grid(row=0, column=1)
        self.search_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        # Init the results frame;
        self.results_frame = gui.ScrollFrameWidget(master=self, width=470, height=750)
        self.results_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        # Internal dict of results;
        self.search_results: Dict[str, 'IngredientSearchResultWidget'] = {}
        # Place to store name of currently selected result;
        self.current_ingredient_name: Optional[str] = None

    def add_result(self, ingredient_name: str) -> None:
        """Adds an ingredient search result widget to the UI."""
        # Check the ingredient isn't listed already;
        if ingredient_name in self.search_results.keys():
            raise ValueError(f"{ingredient_name} is already in results list.")
        # Create the widget;
        ingredient_result_widget = IngredientSearchResultWidget(master=self.results_frame.scrollable_frame,
                                                                ingredient_name=ingredient_name)

        # Bind to edit handler;
        def _on_edit_click(_):  # Closure
            self.current_ingredient_name = ingredient_name
            self.event_generate("<<Edit-Result-Click>>")

        ingredient_result_widget.edit_button.bind("<Button-1>", _on_edit_click)
        ingredient_result_widget.pack()

    def clear_results(self) -> None:
        """Clear all results widgets from the results pane."""
        # Clear the dict in memory;
        self.search_results = {}
        # Clear the UI element;
        for child in self.results_frame.scrollable_frame.winfo_children():
            child.pack_forget()


class IngredientSearchWidgetController:
    def __init__(self, app: 'gui.App', ingredient_search_widget: 'IngredientSearchWidget'):
        self._app = app
        self._ingredient_search_widget = ingredient_search_widget
        # Bind search change to empty box;
        self._ingredient_search_widget.search_entry.bind("<<Value-Changed>>", self._on_search_value_change)
        # Bind search function to search press;
        self._ingredient_search_widget.search_button.bind("<Button-1>", self._on_search_click)
        # Bind result edit handler;
        self._ingredient_search_widget.bind("<<Edit-Result-Click>>", self._on_result_edit_click)

        # Set the search to empty to trigger change event and load all ingredients;
        self._ingredient_search_widget.search_entry.set("")
        self._on_search_value_change(None)

    def load_results(self, ingredient_names: List[str]) -> None:
        """Load search results into the widget."""
        self._ingredient_search_widget.clear_results()
        for ingredient_name in ingredient_names:
            self._ingredient_search_widget.add_result(ingredient_name)

    def _on_result_edit_click(self, event) -> None:
        """Handler for a search result click."""
        # Grab the ingredient from the database;
        i = persistence.load(model.ingredients.Ingredient,
                             unique_value=self._ingredient_search_widget.current_ingredient_name)
        self._app.existing_ingredient_editor.subject = i
        self._app.set_current_view(self._app.existing_ingredient_editor_view, "Edit Ingredient")

    def _on_result_delete_click(self, _) -> None:
        """Handler for deleting an ingredient."""

    def _on_search_click(self, _) -> None:
        """Handler for search click."""
        result_names = persistence.search_for_unique_values(
            subject_type=model.ingredients.Ingredient,
            search_name=self._ingredient_search_widget.search_entry.get(),
            num_results=29
        )
        self.load_results(result_names)

    def _on_search_value_change(self, _) -> None:
        """Handler for search value change."""
        # If the search bar is empty, just show all the ingredients;
        if self._ingredient_search_widget.search_entry.get() == "":
            self.load_results(persistence.get_saved_unique_values(model.ingredients.Ingredient))
        else:
            result_names = persistence.search_for_unique_values(
                subject_type=model.ingredients.Ingredient,
                search_name=self._ingredient_search_widget.search_entry.get(),
                num_results=29
            )
            self.load_results(result_names)
