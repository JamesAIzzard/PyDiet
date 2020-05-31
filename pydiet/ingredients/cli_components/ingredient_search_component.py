from pyconsoleapp import ConsoleAppComponent

from pydiet.ingredients import ingredient_service as igs
from pydiet.ingredients import ingredient_edit_service as ies

_TEMPLATE = '''Ingredient Search: 
------------------

Enter ingredient name and press enter: '''


class IngredientSearchComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self._ies = ies.IngredientEditService()

    def print(self):
        return self.app.fetch_component('standard_page_component').print(_TEMPLATE)

    def dynamic_response(self, response):
        self._ies.ingredient_search_results = igs.get_matching_ingredient_names(
            response, 5)
        self.app.goto('home.ingredients.search_results')
