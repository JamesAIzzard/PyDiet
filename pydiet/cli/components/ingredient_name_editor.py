from typing import TYPE_CHECKING
from pyconsoleapp.console_app_component import ConsoleAppComponent
from pinjector.injector import injector
if TYPE_CHECKING:
    from pydiet.ingredients.ingredient_service import IngredientService

_TEMPLATE = '''Enter ingredient name:
'''

class IngredientNameEditor(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self._ingredient_service:'IngredientService' = \
            injector.inject('IngredientService')

    def run(self):
        output = _TEMPLATE
        output = self.run_parent('StandardPage', output)
        return output

    def dynamic_response(self, response):
        self._ingredient_service.current_ingredient.name = response
        self.app.navigate_back()

ingredient_name_editor = IngredientNameEditor()