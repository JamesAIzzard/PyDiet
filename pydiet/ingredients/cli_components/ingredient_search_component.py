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
        # If we are viewing and editing ingredients;
        if 'home.ingredients.search' in self.app.route:
            self.app.goto('home.ingredients.search_results')
        # If we are deleting ingredients;
        elif 'home.ingredients.delete' in self.app.route:
            self.app.goto('home.ingredients.delete.search_results')
        # If we are building a recipe;
        elif 'home.recipes.edit.ingredients' in self.app.route:
            self.app.goto('home.recipes.edit.ingredients.search_results')
