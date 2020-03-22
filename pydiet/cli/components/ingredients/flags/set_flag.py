from typing import TYPE_CHECKING
from pyconsoleapp import ConsoleAppComponent
from pinjector import inject
if TYPE_CHECKING:
    from pydiet.ingredients.ingredient_service import IngredientService

_TEMPLATE = '\nIs {ingredient_name} {flag}?  (y)/(n)\n\n'


class SetFlag(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self._ingredient_service:'IngredientService' = inject('ingredient_service')
        self.set_option_response('y', self.on_yes)
        self.set_option_response('n', self.on_no)
        self.scope = self.get_scope('ingredient_edit')

    def print(self):
        output = _TEMPLATE.format(ingredient_name=self.scope.ingredient.name, \
            flag=self.scope.current_flag_name(self.scope)).replace('_', ' ')
        output = self.app.get_component('StandardPage').print(output)
        return output

    def on_yes(self):
        self.scope.ingredient.set_flag(\
            self.scope.current_flag_name(self.scope), True)
        self.next()

    def on_no(self):
        self.scope.ingredient.set_flag(\
            self.scope.current_flag_name(self.scope), False)
        self.next()
    
    def next(self):
        # Update the display;
        self.app.set_window_text(self._ingredient_service.\
            summarise_ingredient(self.scope.ingredient))
        # If cycling, update the current flag number,
        # or complete cycle;
        if self.scope.cycling_flags:
            if self.scope.current_flag_number < len(self.scope.flag_number_map):
                self.scope.current_flag_number = self.scope.current_flag_number + 1
                self.app.navigate_back()
                self.app.navigate(['.', 'set'])
            else:
                self.scope.current_flag_number = 0
                self.scope.cycling_flags = False
                self.app.navigate_back()
                self.app.navigate(['.', 'flags_are_set'])
        # Not cycling, just reset the current flag number and
        # go back to the flags menu;
        else:
            self.scope.current_flag_number = 0
            self.app.navigate_back()

