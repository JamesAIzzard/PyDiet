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
        # Build the output;
        output = _TEMPLATE
        output = self.app.fetch_component(
            'standard_page_component').call_print(output)
        # If we are naming for the first time;
        if self._res.recipe.name == None:
            return output
        # If we are editing an existing name;
        else:
            return output, self._res.recipe.name

    def dynamic_response(self, response):
        # If the name has been changed;
        if not response == self._res.recipe.name:
            # Check the another recipe doesn't have this name;
            if rcs.recipe_name_used(response, self._res.datafile_name):
                self.app.error_message = 'There is already a recipe called {}'.\
                    format(response)
                return
            # Update the name
            self._res.recipe.name = response
        # Go back one level;
        self.app.goto('..')
