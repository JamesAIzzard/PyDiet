import tkinter as tk

import gui


class RecipeEditorView(tk.Frame):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class RecipeEditorController(gui.BaseController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def view(self) -> 'RecipeEditorView':
        return super().view

    def update_view(self, *args, **kwargs) -> None:
        pass

    def process_view_changes(self, *args, **kwargs) -> None:
        pass
