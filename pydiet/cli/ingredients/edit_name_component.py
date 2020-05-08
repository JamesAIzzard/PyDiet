from typing import TYPE_CHECKING
from pyconsoleapp.console_app_component import ConsoleAppComponent
from pinjector import inject
if TYPE_CHECKING:
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService
    from pydiet.ingredients import ingredient_service

_TEMPLATE = '''Enter ingredient name:
'''


class EditNameComponent(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self._ies: 'IngredientEditService' = inject(
            'pydiet.cli.ingredient_edit_service')
        self._igs: 'ingredient_service' = inject('pydiet.ingredient_service')

    def print(self):
        output = _TEMPLATE
        output = self.app.get_component(
            'standard_page_component').print(output)
        return output

    def dynamic_response(self, response):
        # If the name has been changed;
        if not response == self._ies.datafile_name:
            # Check the another ingredient doesn't have this name;
            if self._igs.ingredient_name_used(response, self._ies.datafile_name):
                self.app.error_message = 'There is already an ingredient called {}'.\
                    format(response)
                return
            # Update the name
            self._ies.ingredient.name = response
        # Go back one level;
        self.goto('..')
