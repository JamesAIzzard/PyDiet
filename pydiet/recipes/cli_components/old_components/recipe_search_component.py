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
        return self.app.fetch_component('standard_page_component').call_print(_TEMPLATE)

    def dynamic_response(self, response):
        # Load the matching recipe names;
        self._res.recipe_name_search_results = rcs.get_matching_recipe_names(
            response, 5)
        # If we are viewing and editing recipes;
        if 'home.recipes.search' in self.app.route:
            self.app.goto('home.recipes.search_results')
        # If we are deleting recipes;
        elif 'home.recipes.delete' in self.app.route:
            self.app.goto('home.recipes.delete.search_results')
        
