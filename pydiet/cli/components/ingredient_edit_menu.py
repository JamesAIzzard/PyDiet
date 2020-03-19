from typing import TYPE_CHECKING
from pinjector.injector import injector
from pyconsoleapp.console_app_component import ConsoleAppComponent
if TYPE_CHECKING:
    from pydiet.ingredients.ingredient_service import IngredientService

_TEMPLATE = '''Choose an option:
(s) - Save the ingredient.
(1) - Set ingredient name.
(2) - Set ingredient flags.
(3) - Set a macronutrient.
(4) - Set a micronutrient.
'''

class IngredientEditMenu(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self.set_option_response('1', self.on_set_name)
        self.set_option_response('2', self.on_set_flags)
        self.guard_route = ['home', 'ingredients', 'new']
        self._ingredient_service:'IngredientService' = injector.inject('IngredientService')

    def _check_name(self)->bool:
        if not self._ingredient_service.current_ingredient.name:
            self.app.error_message = 'Ingredient name must be set first.'
            return False
        else:
            return True

    def run(self):
        # Check current ingredient is set;
        if not self._ingredient_service.current_ingredient:
            raise NameError('The current ingredient is not defined.')
        # Set the guard to remind the user to save when they leave;
        self.app.guard_exit(self.guard_route, 'IngredientSaveCheck')
        # Update the summary in the window;
        self.app.set_window_text(self._ingredient_service.summarise_ingredient(
            self._ingredient_service.current_ingredient
        ))
        self.app.show_text_window()
        # Draw the view;       
        output = _TEMPLATE
        output = self.run_parent('StandardPage', output)
        return output

    def on_set_name(self):
        self.app.navigate(['.', 'name'])

    def on_set_flags(self):
        if self._check_name():
            self.app.reset_component('IngredientFlagEditor')
            self.app.navigate(['.', 'flags'])
