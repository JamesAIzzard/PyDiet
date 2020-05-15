from typing import TYPE_CHECKING

from pyconsoleapp.console_app_component import ConsoleAppComponent
from pinjector import inject

if TYPE_CHECKING:
    from pydiet.cli.recipes.recipe_edit_service import RecipeEditService
    from pydiet.recipes import recipe_service

_TEMPLATE = '''Enter recipe name:
'''


class EditRecipeNameComponent(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self._res: 'RecipeEditService' = inject(
            'pydiet.cli.recipe_edit_service')
        self._rcs: 'recipe_service' = inject('pydiet.recipe_service')

    def print(self):
        output = _TEMPLATE
        output = self.app.fetch_component(
            'standard_page_component').print(output)
        return output

    def dynamic_response(self, response):
        # If the name has been changed;
        if not response == self._res.datafile_name:
            # Check the another recipe doesn't have this name;
            if self._rcs.recipe_name_used(response, self._res.datafile_name):
                self.app.error_message = 'There is already an recipe called {}'.\
                    format(response)
                return
            # Update the name
            self._res.recipe.name = response
        # Go back one level;
        self.app.goto('..')
