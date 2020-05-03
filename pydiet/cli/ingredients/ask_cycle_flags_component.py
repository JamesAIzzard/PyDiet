from typing import TYPE_CHECKING

from pinjector import inject

from pyconsoleapp import ConsoleAppComponent

if TYPE_CHECKING:
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

_TEMPLATE = '\nSet all flags now? (y)/(n)\n\n'

class AskCycleFlagsComponent(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self._ies:'IngredientEditService' = inject('pydiet.cli.ingredient_edit_service')
        self.set_option_response('y', self.on_yes_set_all)
        self.set_option_response('n', self.on_no_dont_set_all)

    def print(self):
        output = _TEMPLATE
        output = self.get_component('standard_page_component').print(output)
        return output

    def on_yes_set_all(self):
        self._ies.current_flag_number = 1
        self._ies.cycling_flags = True
        self.goto('..edit_flag')

    def on_no_dont_set_all(self):
        self.goto('...flags')