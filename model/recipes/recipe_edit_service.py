from typing import TYPE_CHECKING, Optional, List, Dict

from singleton_decorator import singleton
from pyconsoleapp import menu_tools

import pydiet
from pydiet.recipes import recipe_service as rcs
from pydiet import configs

if TYPE_CHECKING:
    from pydiet.recipes.old_recipe import Recipe
    from pydiet.ingredients.ingredient_amount import IngredientAmount

@singleton
class RecipeEditService():

    def __init__(self):
        self.recipe: Optional['Recipe'] = None
        self.ingredient_amount: Optional['IngredientAmount']
        self.datafile_name: Optional[str] = None
        self.recipe_name_search_results:List[str] = []
        self.selected_serve_time_index:Optional[int] = None
        self.selected_step_number:Optional[int] = None

    @property
    def recipe_search_result_number_name_map(self) -> Dict[int, str]:
        return menu_tools.create_number_name_map(self.recipe_name_search_results)

    @property
    def serve_time_number_map(self) -> Dict[int, str]:
        return menu_tools.create_number_name_map(self.recipe.serve_intervals)

    @property
    def preset_serve_time_number_map(self) -> Dict[int, str]:
        return menu_tools.create_number_name_map(list(configs.PRESET_SERVE_TIMES.keys()))

    def save_changes(self) -> None:
        # Check there is a recipe loaded;
        if not self.recipe:
            raise AttributeError
        # If creating the recipe for the first time;
        if not self.datafile_name:
            # Create the new datafile and stash the name;
            self.datafile_name = rcs.save_new_recipe(self.recipe)
            # Confirm the save;
            pydiet.app.info_message = "Recipe saved."
        # If updating an existing datafile;
        else:
            # Update the recipe;
            rcs.update_existing_recipe(
                self.recipe,
                self.datafile_name
            )
            # Confirm save;
            pydiet.app.info_message = "Recipe saved."
