from typing import TYPE_CHECKING, Optional, List, Dict

from singleton_decorator import singleton
from pinjector import inject

from pydiet.recipes import recipe_service as rcs
from pydiet.shared import configs as cfg
from pydiet.cli.shared import utility_service as cut

if TYPE_CHECKING:
    from pyconsoleapp.console_app import ConsoleApp
    from pydiet.recipes.recipe import Recipe

@singleton
class RecipeEditService():

    def __init__(self):
        self._app:'ConsoleApp' = inject('pydiet.cli.app')
        self.recipe: Optional['Recipe'] = None
        self.datafile_name: Optional[str] = None
        self.mode:str = 'edit'
        self.recipe_name_search_results:List[str] = []

    @property
    def recipe_search_result_number_name_map(self) -> Dict[int, str]:
        return cut.create_number_name_map(self.recipe_name_search_results)

    @property
    def serve_time_number_map(self) -> Dict[int, str]:
        return cut.create_number_name_map(self.recipe.serve_intervals)

    @property
    def preset_serve_time_number_map(self) -> Dict[int, str]:
        return cut.create_number_name_map(list(cfg.PRESET_SERVE_TIMES.keys()))

    def save_changes(self) -> None:
        # Check there is a recipe loaded;
        if not self.recipe:
            raise AttributeError
        # If creating the recipe for the first time;
        if not self.datafile_name:
            # Create the new datafile and stash the name;
            self.datafile_name = rcs.save_new_recipe(self.recipe)
            # Confirm the save;
            self._app.info_message = "Recipe saved."
        # If updating an existing datafile;
        else:
            # Update the recipe;
            rcs.update_existing_recipe(
                self.recipe,
                self.datafile_name
            )
            # Confirm save;
            self._app.info_message = "Recipe saved."
