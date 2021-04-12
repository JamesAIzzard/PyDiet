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
        self.new_ingredient_editor_view = gui.IngredientEditorView(master=self._view_pane)
        self.new_ingredient_editor_controller = gui.IngredientEditorController(
            view=self.new_ingredient_editor_view)
        self.new_ingredient_editor_controller.set_subject(model.ingredients.Ingredient())

        # # Existing ingredient editor;
        # self.existing_ingredient_editor_view = gui.IngredientEditorView(master=self._view_pane)
        # self.existing_ingredient_editor = gui.IngredientEditorWidgetController(
        #     ingredient_editor_widget=self.existing_ingredient_editor_view
        # )
        #
        # # Ingredient search page;
        # self.ingredient_search_view = gui.IngredientSearchWidget(master=self._view_pane)
        # self.ingredient_search = gui.IngredientSearchWidgetController(
        #     app=self,
        #     ingredient_search_widget=self.ingredient_search_view)

        # Load the app showing the new ingredient editor;
        self.set_current_view(self.new_ingredient_editor_view, "Ingredient Search")

    @property
    def root(self) -> 'tk.Tk':
        """Returns the app root instance."""
        return self._root

    def set_current_view(self, view: 'tk.Widget', title: str) -> None:
        """Places the specified widget in the view pane."""
        # Clear the old view;
        for child_view in self._view_pane.winfo_children():
            child_view.pack_forget()
        view.pack(expand=True, fill=tk.BOTH)
        # Set the window title;
        self._root.title(f"PyDiet - {title}")

    def run(self) -> None:
        """Runs the app."""
        self._root.mainloop()
