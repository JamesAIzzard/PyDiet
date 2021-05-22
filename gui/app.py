import tkinter as tk
from typing import Optional

import gui
import model
import persistence


class AppView:
    """View for the main application."""

    def __init__(self):
        self.root = tk.Tk()

        # Init the main view pane;
        self.page_frame = tk.Frame(master=self.root)
        # Init the top menu bar;
        self.top_menu_view = gui.TopMenuView(root=self.root)
        # Now init the pages;
        self.ingredient_editor_view = gui.IngredientEditorView(master=self.page_frame)
        self.ingredient_search_view = gui.IngredientSearchView(master=self.page_frame)
        self.recipe_editor_view = gui.RecipeEditorView(master=self.page_frame)

        # Pack;
        self.page_frame.pack(expand=True, fild=tk.BOTH)


class AppController(gui.BaseController):
    """Controller for the main application."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Init the main window;
        self.view.root.geometry("{}x{}".format(gui.configs.app_window_width, gui.configs.app_widow_height))
        self.view.root.iconbitmap("gui/assets/pydiet.ico")

        # Init the top menu;
        self.top_menu = gui.TopMenuController(app=self.view, view=self.view.top_menu_view)
        # Init the main pages;
        self.ingredient_editor = gui.IngredientEditorController(view=self.view.ingredient_editor_view)
        self.ingredient_search = gui.IngredientSearchController(view=self.view.ingredient_search_view)
        self.recipe_editor = gui.RecipeEditorController(view=self.view.recipe_editor_view)

        # Ref for the current page;
        self._current_page: Optional['gui.AppPage'] = None

        # Load up the current page;
        self.show_page(self.ingredient_search)

    @property
    def view(self) -> 'AppView':
        return super().view

    def set_title(self, title: str) -> None:
        """Sets the title of the main window."""
        self.view.root.title(f"PyDiet - {title}")

    def show_page(self, page: 'gui.AppPage') -> None:
        """Shows the page specified in the app."""
        # Try close the current page;
        try:
            self._current_page.on_page_close()
        # Give up if it throws an exception;
        except gui.exceptions.PageCloseError:
            return
        # Page closed OK, go ahead and pack the new one;
        for view in self.view.page_frame.winfo_children():
            view.pack_forget()
        page.view.pack(expand=True, fill=tk.BOTH)
        self.set_title(page.title)
        page.on_page_load()

    def update_view(self, *args, **kwargs) -> None:
        pass

    def process_view_changes(self, *args, **kwargs) -> None:
        pass


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

        # Ref to current view;
        self.current_view = None

        # Top menu bar;
        self.top_menu_view = gui.TopMenuView(root=self._root)
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

        # Recipe Editor
        self.recipe_editor = gui.RecipeEditorController(
            view=gui.RecipeEditorView(master=self._view_pane)
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
        self.current_view = view
        view.pack(expand=True, fill=tk.BOTH)
        # Set the window title;
        self._root.title(f"PyDiet - {title}")
        # Hack to stop the weird name error bug;
        if isinstance(view, gui.IngredientEditorView):
            view.name_entry.make_valid()

    def _on_ingredient_edit(self, event):
        """Handler for the edit ingredient event."""
        i = persistence.load_instance(
            cls=model.ingredients.Ingredient,
            unique_value=event.widget.ingredient_name
        )
        self.ingredient_editor.set_subject(i)
        self.set_current_view(self.ingredient_editor.view, "Ingredient Editor")

    def run(self) -> None:
        """Runs the app."""
        self._root.mainloop()
