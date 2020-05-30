from pyconsoleapp import ConsoleAppComponent

from pydiet.cli.ingredients import ingredient_edit_service as ies
from pydiet.ingredients import ingredient_service as igs

_TEMPLATE = '''Nutrient Search:
----------------

Enter nutrient name and press enter: '''


class IngredientNutrientSearchComponent(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self._ies = ies.IngredientEditService()

    def print(self):
        return self.app.fetch_component('standard_page_component').print(_TEMPLATE)

    def dynamic_response(self, response):
        self._ies.nutrient_name_search_results = \
            igs.get_matching_nutrient_names(response, 5)
        self.app.goto('home.ingredients.edit.nutrients.search_results')
