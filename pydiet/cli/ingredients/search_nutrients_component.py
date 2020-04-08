from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent
from pinjector import inject

if TYPE_CHECKING:
    from pydiet.ingredients import ingredient_service
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

_TEMPLATE = '''Enter nutrient name:
'''

class NutrientSearchComponent(ConsoleAppComponent):
    def print(self):
        return _TEMPLATE

    def dynamic_response(self, response):
        igs:'ingredient_service' = inject('pydiet.ingredient_service')
        ies:'IngredientEditService' = inject('pydiet.cli.ingredient_edit_service')
        ies.nutrient_name_search_results = igs.get_matching_nutrient_names(response, 4)
        self.goto('..nutrient_search_results')