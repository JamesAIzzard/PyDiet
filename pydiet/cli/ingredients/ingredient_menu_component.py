from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent
from pinjector import inject

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient_service import IngredientService
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

_MENU_TEMPLATE = '''Choose an option:
(1) - Create a new ingredient.
(2) - Edit an existing ingredient.
(3) - Delete an existing ingredient.
(4) - View an existing ingredient.
'''


class IngredientMenuComponent(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self._ingredient_service:'IngredientService' = inject(
            'pydiet.ingredient_service')
        self._edit_service: 'IngredientEditService' = inject(
            'pydiet.ingredient_edit_service')
        self.set_option_response('1', self.on_create)
        self.set_option_response('2', self.on_edit)
        self.set_option_response('3', self.on_delete)
        self.set_option_response('4', self.on_view)

    def print(self):
        output = _MENU_TEMPLATE
        output = self.app.get_component('StandardPageComponent').print(output)
        return output

    def on_create(self):
        # Put a fresh ingredient on the scope;
        self._edit_service.ingredient = \
            self._ingredient_service.get_new_ingredient()
        # Guard the exit to prompt saving when returning from create;
        self.get_component('IngredientSaveCheckComponent').guarded_route = \
            'home.ingredients.new'
        self.guard_exit('home.ingredients.new', 'IngredientSaveCheckComponent')
        # Go;
        self.goto('.new')

    def on_edit(self):
        raise NotImplementedError

    def on_delete(self):
        raise NotImplementedError

    def on_view(self):
        raise NotImplementedError
