from typing import TYPE_CHECKING

from pinjector import inject

from pyconsoleapp import ConsoleAppComponent

if TYPE_CHECKING:
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

_FLAG_MENU = '''Choose a flag to edit:
{}
'''
_FLAG_MENU_ITEM = '({flag_number}) - {flag}\n'

class IngredientFlagMenuComponent(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self._scope:'IngredientEditService' = inject('pydiet.ingredient_edit_service')

    def print(self):
        flags_menu = ''
        for flag_number in self._scope.flag_number_name_map.keys():
            flags_menu = flags_menu + _FLAG_MENU_ITEM.format(
                flag_number = flag_number,
                flag = self._scope.flag_name_from_number(flag_number).replace('_', ' ')
            )
        output = _FLAG_MENU.format(flags_menu)
        output = self.get_component('StandardPageComponent').print(output)
        return output

    def dynamic_response(self, response):
        # Try and parse the response as an integer;
        try:
            response = int(response)
        except ValueError:
            return
        # Conversion went OK, so set flag number from response;
        if response in self._scope.flag_number_name_map.keys():
            self._scope.current_flag_number = response
        # And nav to set flag;      
        self.goto('.set')
