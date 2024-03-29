import tkinter as tk

import gui


class FlagNutrientStatusView(tk.LabelFrame):
    def __init__(self, **kwargs):
        super().__init__(text="Nutrient-Flag Status", **kwargs)
        self.status_label = tk.Label(master=self, text="")
        self.status_label.grid(row=0, column=0, sticky="w")


class FlagNutrientStatusController(gui.BaseController):
    def __init__(self, view: 'FlagNutrientStatusView', **kwargs):
        super().__init__(view=view, **kwargs)
        self._has_conflict: bool = False

    def show_ok(self) -> None:
        """Change the state to no-conflict."""
        self.view.status_label.configure(text="No conflicts.", fg="green")
        self._has_conflict = False

    def show_conflict(self, conflict_message: str) -> None:
        """Change state to show conflict."""
        self.view.status_label.configure(text=conflict_message, fg="red")
        self._has_conflict = True

    @property
    def has_conflict(self) -> bool:
        """Returns True/False to indicate if a conflict is logged."""
        return self._has_conflict

    @property
    def view(self) -> 'FlagNutrientStatusView':
        return super().view

    def update_view(self) -> None:
        pass

    def process_view_changes(self, *args, **kwargs) -> None:
        pass
