from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent
from pinjector import inject

if TYPE_CHECKING:
    from pydiet.recipes import recipe_service
    from pydiet.cli.recipes.recipe_edit_service import RecipeEditService

_TEMPLATE = '''
Recipe Search: 
--------------

Enter recipe name and press enter: '''


class RecipeSearchComponent(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self._rcs: 'recipe_service' = inject('pydiet.recipe_service')
        self._res: 'RecipeEditService' = inject(
            'pydiet.cli.recipe_edit_service')

    def print(self):
        return self.app.fetch_component('standard_page_component').print(_TEMPLATE)

    def dynamic_response(self, response):
        self._res.recipe_name_search_results = self._rcs.get_matching_recipe_names(
            response, 5)
        self.app.goto('home.recipes.search_results')
