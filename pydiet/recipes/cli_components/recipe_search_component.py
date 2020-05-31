from pyconsoleapp import ConsoleAppComponent

from pydiet.recipes import recipe_service as rcs
from pydiet.recipes import recipe_edit_service as res

_TEMPLATE = '''
Recipe Search: 
--------------

Enter recipe name and press enter: '''


class RecipeSearchComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self._res = res.RecipeEditService()

    def print(self):
        return self.app.fetch_component('standard_page_component').print(_TEMPLATE)

    def dynamic_response(self, response):
        self._res.recipe_name_search_results = rcs.get_matching_recipe_names(
            response, 5)
        self.app.goto('home.recipes.search_results')
