import tkinter as tk
from tkinter import messagebox

import gui
import model.ingredients


class TopMenuWidget(tk.Menu):
    def __init__(self, root, **kwargs):
        super().__init__(master=root, **kwargs)
        self._root = root
        self._menu = tk.Menu()
        self._root.config(menu=self._menu)

        # Ingredients;
        self._ingredients_menu = tk.Menu(self._root, tearoff=False)
        self._menu.add_cascade(label="Ingredients", menu=self._ingredients_menu)
        self._ingredients_menu.add_command(label="New",
                                           command=lambda: self._root.event_generate("<<New-Ingredient-Click>>"))
        self._ingredients_menu.add_command(label="Edit",
                                           command=lambda: self._root.event_generate("<<Edit-Ingredient-Click>>"))
        self._ingredients_menu.add_command(label="View",
                                           command=lambda: self._root.event_generate("<<View-Ingredients-Click>>"))

        # Recipes;
        self._recipes_menu = tk.Menu(self._root, tearoff=False)
        self._menu.add_cascade(label="Recipes", menu=self._recipes_menu)
        self._recipes_menu.add_command(label="New",
                                       command=lambda: self._root.event_generate("<<New-Recipe-Click>>"))
        self._recipes_menu.add_command(label="Edit",
                                       command=lambda: self._root.event_generate("<<Edit-Recipe-Click>>"))
        self._recipes_menu.add_command(label="View",
                                       command=lambda: self._root.event_generate("<<View-Recipes-Click>>"))

        # Goals;
        self._goals_menu = tk.Menu(self._root, tearoff=False)
        self._menu.add_cascade(label="Goals", menu=self._goals_menu)
        self._goals_menu.add_command(label="Edit Global Day Goals",
                                     command=lambda: self._root.event_generate("<<Edit-Global-Day-Goals-Click>>"))
        self._goals_menu.add_command(label="New Day Goal",
                                     command=lambda: self._root.event_generate("<<New-Day-Goal-Click>>"))
        self._goals_menu.add_command(label="Edit Day Goal",
                                     command=lambda: self._root.event_generate("<<Edit-Day-Goal-Click>>"))
        self._goals_menu.add_command(label="View Day Goals",
                                     command=lambda: self._root.event_generate("<<View-Day-Goal-Click>>"))
        self._goals_menu.add_command(label="New Meal Goal",
                                     command=lambda: self._root.event_generate("<<New-Meal-Goal-Click>>"))
        self._goals_menu.add_command(label="Edit Meal Goal",
                                     command=lambda: self._root.event_generate("<<Edit-Meal-Goal-Click>>"))
        self._goals_menu.add_command(label="View Meal Goals",
                                     command=lambda: self._root.event_generate("<<Edit-Day-Goal-Click>>"))

        # Solve;
        self._solve_menu = tk.Menu(self._root)
        self._menu.add_command(label="Solve",
                               command=lambda: self._root.event_generate("<<Solve-Click>>"))


class TopMenuController:
    def __init__(self, app: 'gui.App', view: 'TopMenuWidget'):
        self._app = app
        self._view = view
        self._app.root.bind("<<New-Ingredient-Click>>", self._on_new_ingredient_click)
        self._app.root.bind("<<Edit-Ingredient-Click>>", self._on_edit_ingredient_click)
        self._app.root.bind("<<View-Ingredients-Click>>", self._on_view_ingredients_click)
        self._app.root.bind("<<New-Recipe-Click>>", self._on_new_recipe_click)
        self._app.root.bind("<<Edit-Recipe-Click>>", self._on_edit_recipe_click)
        self._app.root.bind("<<View-Recipes-Click>>", self._on_view_recipes_click)
        self._app.root.bind("<<Edit-Global-Day-Goals-Click>>", self._on_edit_global_day_goals_click)
        self._app.root.bind("<<New-Day-Goasl-Click>>", self._on_new_day_goals_click)
        self._app.root.bind("<<Edit-Day-Goals-Click>>", self._on_edit_day_goals_click)
        self._app.root.bind("<<New-Meal-Goals-Click>>", self._on_new_meal_goals_click)
        self._app.root.bind("<<Edit-Meal-Goals-Click>>", self._on_edit_meal_goals_click)
        self._app.root.bind("<<Solve-Click>>", self._on_solve_click)

    def _check_save(self) -> bool:
        if isinstance(self._app.current_view, gui.IngredientEditorView):
            if self._app.ingredient_editor.subject is None:
                return True
            elif self._app.ingredient_editor.subject.has_unsaved_changes:
                response = messagebox.askyesno(title="PyDiet", message="Save changes to ingredient?")
                if response is True:
                    return self._app.ingredient_editor._on_save_clicked(None)
        return True

    def _on_new_ingredient_click(self, _):
        if self._check_save():
            self._app.ingredient_editor.set_subject(model.ingredients.Ingredient())
            self._app.set_current_view(self._app.ingredient_editor.view, "New Ingredient")

    def _on_edit_ingredient_click(self, _):
        if self._check_save():
            self._app.set_current_view(self._app.ingredient_search.view, "Ingredient Search")
            self._app.ingredient_search.process_view_changes()

    def _on_view_ingredients_click(self, _):
        if self._check_save():
            self._app.set_current_view(self._app.ingredient_search.view, "Ingredient Search")
            self._app.ingredient_search.process_view_changes()

    @staticmethod
    def _on_new_recipe_click(_):
        print("New Recipe Nav Clicked")

    @staticmethod
    def _on_edit_recipe_click(_):
        print("Edit Recipe Nav Clicked")

    @staticmethod
    def _on_view_recipes_click(_):
        print("View Recipe Nav Clicked")

    @staticmethod
    def _on_edit_global_day_goals_click(_):
        print("Edit Global Day Goals Clicked")

    @staticmethod
    def _on_new_day_goals_click(_):
        print("New Day Goal Clicked")

    @staticmethod
    def _on_edit_day_goals_click(_):
        print("Edit Day Goal Clicked")

    @staticmethod
    def _on_new_meal_goals_click(_):
        print("New Meal Goal Clicked")

    @staticmethod
    def _on_edit_meal_goals_click(_):
        print("Edit Meal Goal Clicked")

    @staticmethod
    def _on_solve_click(_):
        print("Solve Clicked")
