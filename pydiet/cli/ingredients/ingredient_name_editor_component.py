from typing import TYPE_CHECKING
from pyconsoleapp.console_app_component import ConsoleAppComponent
from pinjector import inject
if TYPE_CHECKING:
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

_TEMPLATE = '''Enter ingredient name:
'''

class IngredientNameEditorComponent(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self._scope:'IngredientEditService' = inject('pydiet.ingredient_edit_service')

    def print(self):
        output = _TEMPLATE
        output = self.app.get_component('standard_page_component').print(output)
        return output

    def dynamic_response(self, response):
        self._scope.ingredient.name = response
        self.app.info_message = 'Ingredient name set successfully.'
        self.goto('..')
