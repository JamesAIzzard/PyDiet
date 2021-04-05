import tkinter as tk

import gui
import model

class App:
    """PyDiet GUI root instance."""

    def __init__(self):
        self._root = tk.Tk()
        self._root.title("PyDiet")
        self._root.geometry("{}x{}".format(gui.configs.app_window_width, gui.configs.app_widow_height))
        self._root.iconbitmap("gui/assets/pydiet.ico")

        # Frame that shows the current page;
        self._view_pane = tk.Frame(master=self._root)
        self._view_pane.pack(expand=True, fill=tk.BOTH)

        # Top menu bar;
        self.top_menu_view = gui.TopMenuWidget(root=self._root)
        self.top_menu = gui.TopMenuController(app=self, view=self.top_menu_view)

        # New ingredient editor;
        self.new_ingredient_editor_view = gui.IngredientEditorWidget(master=self._view_pane)
        self.new_ingredient_editor = gui.IngredientEditorController(app=self, view=self.new_ingredient_editor_view)

        # Load the app showing the new ingredient editor;
        self.set_current_view(self.new_ingredient_editor_view)
        self.new_ingredient_editor.subject = model.ingredients.Ingredient()

    @property
    def root(self) -> 'tk.Tk':
        """Returns the app root instance."""
        return self._root

    def set_current_view(self, view: 'tk.Widget') -> None:  # noqa
        """Places the specified widget in the view pane."""
        view.pack(expand=True, fill=tk.BOTH)

    def run(self) -> None:
        """Runs the app."""
        self._root.mainloop()
