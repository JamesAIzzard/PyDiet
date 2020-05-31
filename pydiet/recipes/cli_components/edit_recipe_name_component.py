from pyconsoleapp import ConsoleAppComponent

from pydiet.recipes import recipe_edit_service as res
from pydiet.recipes import recipe_service as rcs

_TEMPLATE = '''Enter recipe name:
'''


class EditRecipeNameComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self._res = res.RecipeEditService()

    def print(self):
        output = _TEMPLATE
        output = self.app.fetch_component(
            'standard_page_component').print(output)
        return output

    def dynamic_response(self, response):
        # If the name has been changed;
        if not response == self._res.datafile_name:
            # Check the another recipe doesn't have this name;
            if rcs.recipe_name_used(response, self._res.datafile_name):
                self.app.error_message = 'There is already an recipe called {}'.\
                    format(response)
                return
            # Update the name
            self._res.recipe.name = response
        # Go back one level;
        self.app.goto('..')