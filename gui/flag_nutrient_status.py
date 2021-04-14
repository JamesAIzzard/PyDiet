import tkinter as tk

import gui


class FlagNutrientStatusView(tk.Frame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._heading_label = tk.Label(master=self, text="Flag-Nutrient Status: ")
        self._heading_label.grid(row=0, column=0, sticky="w")
        self.status_label = tk.Label(master=self, text="")
        self.status_label.grid(row=0, column=1, sticky="w")


class FlagNutrientStatusController(gui.BaseController):
    def __init__(self, view: 'FlagNutrientStatusView', **kwargs):
        super().__init__(view=view, **kwargs)

    @property
    def view(self) -> 'FlagNutrientStatusView':
        return super().view

    def update_view(self, status_message: str) -> None:
        self.view.status_label.configure(text=status_message)

    def process_view_changes(self, *args, **kwargs) -> None:
        # Work through the flags, trying to set.
        # Work through the nutrients trying to set.
        # If you find an error, display it;
        pass
