import tkinter as tk
from typing import Callable

import gui
import model.nutrients


class NutrientSearchView(tk.Frame):
    """Search bar and results field to allow the selection of a nutrient."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create the search entry and button;
        self.search_entry = gui.SmartEntryWidget(master=self, width=40)
        self.search_button = tk.Button(master=self, text="Search Nutrients")
        # Create the results box;
        self.results_scrollframe = gui.ScrollFrameWidget(master=self, width=350, height=150)
        # # Build the view up;
        self.search_entry.grid(row=0, column=0, sticky="w")
        self.search_button.grid(row=0, column=1, sticky="w")
        self.results_scrollframe.grid(row=1, column=0, columnspan=2)

    def clear(self) -> None:
        """Clears all nutrient names from the list."""
        for child in self.results_scrollframe.scrollable_frame.winfo_children():
            child.pack_forget()


class NutrientSearchController(gui.BaseController):
    def __init__(self, view: 'NutrientSearchView', on_result_click: Callable[..., None], **kwargs):
        super().__init__(view=view, **kwargs)

        self._on_result_click = on_result_click

        # Bind search events to search handler;
        self.view.search_entry.bind("<<Value-Changed>>", self.process_view_changes)
        self.view.search_button.bind("<Button-1>", self.process_view_changes)

    @property
    def view(self) -> 'NutrientSearchView':
        return super().view

    def add_result(self, nutrient_name: str) -> None:
        """Adds a nutrient name to the list."""
        # Create the result item;
        result = tk.Label(master=self.view.results_scrollframe.scrollable_frame, text=nutrient_name)
        result.nutrient_name = nutrient_name
        # Bind the click responder;
        result.bind("<Button-1>", self._on_result_click)
        # Add it to the search box;
        result.pack()

    def update_view(self, *args, **kwargs) -> None:
        pass

    def process_view_changes(self, *args, **kwargs) -> None:
        self.view.clear()
        matches = model.nutrients.get_n_closest_nutrient_names(self.view.search_entry.get(), num_results=10)
        for nutrient_name in matches:
            self.add_result(nutrient_name)
