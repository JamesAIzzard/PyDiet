from typing import TYPE_CHECKING

from pyconsoleapp.console_app_component import ConsoleAppComponent
from pinjector import inject


if TYPE_CHECKING:
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService
    from pydiet.data import repository_service

_TEMPLATE = '''
    Are you sure you want to delete
    {ingredient_name}?

    (y)es/(n)o

'''

class ConfirmIngredientDeleteComponent(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self._ies:'IngredientEditService' = inject('pydiet.cli.ingredient_edit_service')
        self._rp:'repository_service' = inject('pydiet.repository_service')
        self.set_option_response('y', self.on_yes)
        self.set_option_response('n', self.on_no)

    def print(self):
        output = _TEMPLATE.format(
            ingredient_name=self._ies.ingredient.name
        )
        return self.get_component('standard_page_component').print(output)

    def on_yes(self):
        if self._ies.datafile_name:
            # Delete the datafile;
            self._rp.delete_ingredient_data(self._ies.datafile_name)
            # Set status message;
            self.app.info_message = '{} deleted.'.format(self._ies.ingredient.name)
            # Redirect;
            self.goto('home.ingredients')
        else:
            raise AttributeError

    def on_no(self):
        self.app.info_message = 'Ingredient was not deleted.'
        self.goto('home.ingredients')