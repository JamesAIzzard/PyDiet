from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent
from pinjector import inject

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient_service import IngredientService
    from pydiet.ingredients.ingredient import Ingredient
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

_UNITS_TEMPLATE = '''
    {mass}{units} of {ingredient_name} costs £__.____
                {spacer}^^^^^^^

How much does {mass}{units} of {ingredient_name}
cost?
'''

class SetCostComponent(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self._ingredient_service:'IngredientService' = inject('pydiet.ingredient_service')
        self._scope:'IngredientEditService' = inject('pydiet.ingredient_edit_service')

    def print(self):
        output = _UNITS_TEMPLATE.format(\
            ingredient_name=self._scope.ingredient.name,
            mass=self._scope.temp_cost_mass,
            units=self._scope.temp_cost_mass_units,
            spacer=' '*len(self._scope.ingredient.name+\
                str(self._scope.temp_cost_mass)+self._scope.temp_cost_mass_units)
        )
        output = self.get_component('StandardPageComponent').print(output)
        return output

    def dynamic_response(self, response):
        # Try and convert the response into a cost value;
        cost = None
        try:
            cost = float(response)
        except ValueError:
            self.app.error_message = "Unable to parse {} as a cost. Try again."\
                .format(response)
            return
        # Set all the data and return to the menu;
        self._scope.ingredient.set_cost(
            cost, 
            self._scope.temp_cost_mass, 
            self._scope.temp_cost_mass_units)
        self.app.info_message = 'Cost set successfully.'
        self.goto('..')