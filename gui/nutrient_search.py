import tkinter as tk

import gui


class NutrientSearchView(tk.Frame):
    """Search bar and results field to allow the selection of a nutrient."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create the search entry and button;
        self.search_entry = gui.SmartEntryWidget(master=self, width=30)
        self.search_button = tk.Button(master=self, text="Search Nutrients")
        # Create the results box;
        self._results_scrollframe = gui.ScrollFrameWidget(master=self, width=470, height=150)

        # Build the view up;
        self.search_entry.grid(row=0, column=0)
        self.search_button.grid(row=0, column=1)
        self._results_scrollframe.grid(row=0, column=0, columnspan=2)


class NutrientSearchController(gui.BaseController):
    def __init__(self, view: 'NutrientSearchView', **kwargs):
        super().__init__(view=view, **kwargs)

    @property
    def view(self) -> 'NutrientSearchView':
        return super().view

    def update_view(self, *args, **kwargs) -> None:
        pass

    def process_view_changes(self, *args, **kwargs) -> None:
        pass
