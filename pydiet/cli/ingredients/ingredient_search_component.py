from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent
from pinjector import inject

if TYPE_CHECKING:
    from pydiet.ingredients import ingredient_service
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

_TEMPLATE = '''Ingredient Search: 
------------------

Enter ingredient name and press enter: '''


class IngredientSearchComponent(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self._igs: 'ingredient_service' = inject('pydiet.ingredient_service')
        self._ies: 'IngredientEditService' = inject(
            'pydiet.cli.ingredient_edit_service')

    def print(self):
        return self.get_component('standard_page_component').print(_TEMPLATE)

    def dynamic_response(self, response):
        self._ies.ingredient_search_results = self._igs.get_matching_ingredient_names(
            response, 5)
        self.goto('..search_results')
