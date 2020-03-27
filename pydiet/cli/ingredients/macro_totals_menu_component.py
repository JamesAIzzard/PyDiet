from typing import TYPE_CHECKING

from pinjector import inject

from pyconsoleapp import ConsoleAppComponent

if TYPE_CHECKING:
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

_MACRO_TOTAL_MENU = '''Choose a macronutrient total to edit:
{}
'''
_MACRO_TOTAL_MENU_ITEM = '({number}) - {macro_total_name}\n'


class MacroTotalsMenuComponent(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self._scope: 'IngredientEditService' = inject(
            'pydiet.ingredient_edit_service')

    def print(self):
        totals_menu = ''
        for number in self._scope.current_nutrient_number_name_map.keys():
            totals_menu = totals_menu + _MACRO_TOTAL_MENU_ITEM.format(
                number=number,
                macro_total_name=self._scope.nutrient_name_from_number(number)
            )
        output = _MACRO_TOTAL_MENU.format(totals_menu)
        output = self.get_component('StandardPageComponent').print(output)
        return output

    def dynamic_response(self, response):
        # Try and convert the response to an integer;
        try:
            response = int(response)
        except ValueError:
            return
        # If response matches an option;
        if response in self._scope.current_nutrient_number_name_map.keys():
            # Set the current nutrient number and go ahead to set the sample mass;
            self._scope.current_nutrient_number = response
            self.goto('.sample_mass')
