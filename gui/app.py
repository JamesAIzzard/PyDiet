import tkinter as tk

import gui
import model
import persistence


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

        # ingredient editor;
        self.ingredient_editor = gui.IngredientEditorController(
            view=gui.IngredientEditorView(master=self._view_pane)
        )
        self.ingredient_editor.set_subject(model.ingredients.Ingredient())

        # Ingredient search page;
        self.ingredient_search = gui.IngredientSearchController(
            view=gui.IngredientSearchView(master=self._view_pane),
            on_result_edit_callback=self._on_ingredient_edit
        )

        # Load the app showing the new ingredient editor;
        self.set_current_view(self.ingredient_search.view, "Ingredient Search")

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
        # Hack to stop the weird name error bug;
        if isinstance(view, gui.IngredientEditorView):
            view.name_entry.make_valid()

    def _on_ingredient_edit(self, event):
        """Handler for the edit ingredient event."""
        i = persistence.load(
            cls=model.ingredients.Ingredient,
            unique_value=event.widget.ingredient_name
        )
        self.ingredient_editor.set_subject(i)
        self.set_current_view(self.ingredient_editor.view, "Ingredient Editor")

    def run(self) -> None:
        """Runs the app."""
        self._root.mainloop()
