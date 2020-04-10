from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent
from pinjector import inject

if TYPE_CHECKING:
    from pydiet.ingredients import ingredient_service
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
        self._igs:'ingredient_service' = inject('pydiet.ingredient_service')
        self._ies:'IngredientEditService' = inject('pydiet.cli.ingredient_edit_service')

    def print(self):
        output = _UNITS_TEMPLATE.format(\
            ingredient_name=self._ies.ingredient.name,
            mass=self._ies.temp_cost_mass,
            units=self._ies.temp_cost_mass_units,
            spacer=' '*len(self._ies.ingredient.name+\
                str(self._ies.temp_cost_mass)+self._ies.temp_cost_mass_units)
        )
        output = self.get_component('standard_page_component').print(output)
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
        self._ies.ingredient.set_cost(
            cost, 
            self._ies.temp_cost_mass, 
            self._ies.temp_cost_mass_units)
        self.goto('..')