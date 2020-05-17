from typing import TYPE_CHECKING, Optional, List, Dict

from pinjector import inject

if TYPE_CHECKING:
    from pyconsoleapp.console_app import ConsoleApp
    from pydiet.recipes.recipe import Recipe
    from pydiet.recipes import recipe_service
    from pydiet.shared import configs
    from pydiet.cli.shared import utility_service as cli_utility_service

class RecipeEditService():

    def __init__(self):
        self._rcs:'recipe_service' = inject('pydiet.recipe_service')
        self._cf:'configs' = inject('pydiet.configs')
        self._cli_utils:'cli_utility_service' = inject('pydiet.cli.utility_service')
        self._app:'ConsoleApp' = inject('pydiet.cli.app')
        self.recipe: Optional['Recipe'] = None
        self.datafile_name: Optional[str] = None
        self.mode:str = 'edit'
        self.recipe_name_search_results:List[str] = []

    @property
    def recipe_search_result_number_name_map(self) -> Dict[int, str]:
        return self._cli_utils.create_number_name_map(self.recipe_name_search_results)

    @property
    def serve_time_number_map(self) -> Dict[int, str]:
        return self._cli_utils.create_number_name_map(self.recipe.serve_intervals)

    @property
    def preset_serve_time_number_map(self) -> Dict[int, str]:
        return self._cli_utils.create_number_name_map(list(self._cf.PRESET_SERVE_TIMES.keys()))

    def save_changes(self) -> None:
        # Check there is a recipe loaded;
        if not self.recipe:
            raise AttributeError
        # If creating the recipe for the first time;
        if not self.datafile_name:
            # Create the new datafile and stash the name;
            self.datafile_name = self._rcs.save_new_recipe(self.recipe)
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
