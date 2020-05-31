from pyconsoleapp import ConsoleAppComponent

from pydiet.ingredients import ingredient_edit_service as ies
from pydiet.ingredients import ingredient_service as igs

_TEMPLATE = '''Enter ingredient name:
'''


class EditIngredientNameComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self._ies = ies.IngredientEditService()

    def print(self):
        output = _TEMPLATE
        output = self.app.fetch_component(
            'standard_page_component').print(output)
        return output

    def dynamic_response(self, response):
        # If the name has been changed;
        if not response == self._ies.datafile_name:
            # Check the another ingredient doesn't have this name;
            if igs.ingredient_name_used(response, self._ies.datafile_name):
                self.app.error_message = 'There is already an ingredient called {}'.\
                    format(response)
                return
            # Update the name
            self._ies.ingredient.name = response
        # Go back one level;
        self.app.goto('home.ingredients.edit')
