from typing import TYPE_CHECKING
from pyconsoleapp.console_app_component import ConsoleAppComponent
from pinjector import inject
if TYPE_CHECKING:
    from pydiet.ingredients.ingredient_service import IngredientService

_TEMPLATE = '''Enter ingredient name:
'''

class IngredientNameEditor(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self._ingredient_service:'IngredientService' = inject('ingredient_service')

    def print(self):
        output = _TEMPLATE
        output = self.app.get_component('StandardPage').print(output)
        return output

    def dynamic_response(self, response):
        scope = self.get_scope('ingredient_edit')
        scope.ingredient.name = response
        self.app.info_message = 'Ingredient name set successfully.'
        self.app.set_window_text(self._ingredient_service.\
            summarise_ingredient(scope.ingredient))
        self.app.navigate_back()
