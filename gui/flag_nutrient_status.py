import tkinter as tk

import gui


class FlagNutrientStatusView(tk.Frame):
    pass


class FlagNutrientStatusController(gui.BaseController):
    @property
    def view(self) -> 'Any':
        pass

    def update_view(self, *args, **kwargs) -> None:
        # Work through the flags, trying to set.
        # Work through the nutrients trying to set.
        # If you find an error, display it;
        pass

    def process_view_changes(self, *args, **kwargs) -> None:
        pass
