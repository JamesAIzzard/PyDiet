from typing import TYPE_CHECKING, Optional

from pinjector import inject

from pydiet.cli.recipes.exceptions import UnnamedRecipeError

if TYPE_CHECKING:
    from pyconsoleapp.console_app import ConsoleApp
    from pydiet.recipes.recipe import Recipe
    from pydiet.recipes import recipe_service

class RecipeEditService():

    def __init__(self):
        self._rcs:'recipe_service' = inject('pydiet.recipe_service')
        self._app:'ConsoleApp' = inject('pydiet.cli.app')
        self.recipe: Optional['Recipe']
        self.datafile_name: Optional[str]

    def save_changes(self, redirect_to=None) -> None:
        # Check there is a recipe loaded;
        if not self.recipe:
            raise AttributeError
        # Check the recipe is named;
        if not self.recipe.name:
            raise UnnamedRecipeError
        # If creating the recipe for the first time;
        if not self.datafile_name:
            # Create the new datafile and stash the name;
            self.datafile_name = self._rcs.save_new_recipe(self.recipe)
            # Redirect to edit, now the datafile exists;
            if redirect_to:
                self._app.clear_exit('home.recipes.new')
                self._app.guard_exit('home.ingredients.edit', 'RecipeSaveCheckComponent')
                self._app.goto(redirect_to)
            # Confirm the save;
            self._app.info_message = "Recipe saved."
        # If updating an existing datafile;
        else:
            # Update the recipe;
            self._rcs.update_existing_recipe(
                self.recipe,
                self.datafile_name
            )
            # Confirm save;
            self._app.info_message = "Recipe saved."
