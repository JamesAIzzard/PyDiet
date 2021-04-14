import tkinter as tk
from typing import List, Dict, Callable, Optional

import gui
import model.ingredients
import persistence


class IngredientSearchResultView(tk.Frame):
    def __init__(self, ingredient_name: str, **kwargs):
        super().__init__(**kwargs)
        self.ingredient_name = ingredient_name
        self._ingredient_name_label = tk.Label(master=self, text=ingredient_name, width=60, background="#c0c0c0",
                                               anchor="w")
        self.edit_button = tk.Button(master=self, text="Edit")
        self.delete_button = tk.Button(master=self, text="Delete")
        self._ingredient_name_label.grid(row=0, column=0, sticky="ew")
        self.edit_button.grid(row=0, column=1, sticky="ew")

        # Bind handlers
        self.edit_button.bind("<Button-1>", lambda _: self.event_generate("<Button-1>"))


class IngredientSearchResultController(gui.BaseController):
    def __init__(self, view: 'IngredientSearchResultView', **kwargs):
        super().__init__(view=view, **kwargs)

    @property
    def view(self) -> 'IngredientSearchResultView':
        return self.view

    def update_view(self, *args, **kwargs) -> None:
        pass

    def process_view_changes(self, *args, **kwargs) -> None:
        pass


class IngredientSearchView(tk.Frame):
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

        # Internal dict of result widgets;
        self.search_results: Dict[str, 'IngredientSearchResultView'] = {}
        # Place to store name of currently selected result;
        self.current_ingredient_name: Optional[str] = None

    def add_result(self, ingredient_name: str, on_edit_callback=Callable) -> None:
        """Adds an ingredient search result widget to the UI."""
        # Check the ingredient isn't listed already;
        if ingredient_name in self.search_results.keys():
            raise ValueError(f"{ingredient_name} is already in results list.")
        # Create the widget;
        ingredient_result_widget = IngredientSearchResultView(master=self.results_frame.scrollable_frame,
                                                              ingredient_name=ingredient_name)
        # Bind the edit callback
        ingredient_result_widget.bind("<Button-1>", on_edit_callback)
        ingredient_result_widget.pack()

    def clear_results(self) -> None:
        """Clear all results widgets from the results pane."""
        # Clear the dict in memory;
        self.search_results = {}
        # Clear the UI element;
        for child in self.results_frame.scrollable_frame.winfo_children():
            child.pack_forget()


class IngredientSearchController(gui.BaseController):
    def __init__(self, view: 'IngredientSearchView', on_result_edit_callback: Callable[[], None], **kwargs):
        super().__init__(view=view, **kwargs)

        # Stash the edit callback;
        self._on_result_edit_callback = on_result_edit_callback

        # Bind search change to empty box;
        self.view.search_entry.bind("<<Value-Changed>>", self.process_view_changes)
        # Bind search function to search press;
        self.view.search_button.bind("<Button-1>", self.process_view_changes)

        # Set the search to empty to trigger change event and load all ingredients;
        self.view.search_entry.set("")
        self.process_view_changes()

    @property
    def view(self) -> 'IngredientSearchView':
        return super().view

    def update_view(self, *args, **kwargs) -> None:
        pass

    def process_view_changes(self, *args, **kwargs) -> None:
        # If the search bar is empty, just show all the ingredients;
        if self.view.search_entry.get() == "":
            self.load_results(persistence.get_saved_unique_values(model.ingredients.Ingredient))
        else:
            result_names = persistence.search_for_unique_values(
                subject_type=model.ingredients.Ingredient,
                search_name=self.view.search_entry.get(),
                num_results=29
            )
            self.load_results(result_names)

    def load_results(self, ingredient_names: List[str]) -> None:
        """Load search results into the widget."""
        self.view.clear_results()
        for ingredient_name in ingredient_names:
            self.view.add_result(ingredient_name, self._on_result_edit_callback)
