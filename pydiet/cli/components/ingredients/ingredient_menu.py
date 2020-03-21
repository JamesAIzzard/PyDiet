from typing import TYPE_CHECKING
from pyconsoleapp.console_app_component import ConsoleAppComponent
from pinjector import inject
if TYPE_CHECKING:
    from pydiet.ingredients.ingredient_service import IngredientService

_MENU_TEMPLATE = '''Choose an option:
(1) - Create a new ingredient.
(2) - Edit an existing ingredient.
(3) - Delete an existing ingredient.
(4) - View an existing ingredient.
'''


class IngredientMenu(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self._ingredient_service: IngredientService = inject('ingredient_service')
        self.set_option_response('1', self.on_create)
        self.set_option_response('2', self.on_edit)
        self.set_option_response('3', self.on_delete)
        self.set_option_response('4', self.on_view)


    def print(self):
        output = _MENU_TEMPLATE
        output = self.app.get_component('StandardPage').print(output)
        return output

    def on_create(self):
        # Fresh data scope for new ingredient;
        scope = self.create_scope('ingredient_edit')
        # Place fresh ingredient in the scope;
        scope.ingredient = self._ingredient_service.get_new_ingredient()
        # Configure the exit guard to prompt saving;
        self.app.guard_exit(['.', 'new'], 'IngredientSaveCheck')
        # Update the summary in the window;
        self.app.set_window_text(self._ingredient_service.summarise_ingredient(
            scope.ingredient
        ))
        self.app.show_text_window()
        # Go go go!
        self.app.navigate(['.', 'new'])

    def on_edit(self):
        raise NotImplementedError

    def on_delete(self):
        raise NotImplementedError

    def on_view(self):
        raise NotImplementedError

    def dynamic_response(self, response):
        pass
