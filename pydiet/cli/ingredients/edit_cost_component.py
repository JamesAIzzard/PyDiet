from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent
from pinjector import inject

if TYPE_CHECKING:
    from pydiet.ingredients import ingredient_service
    from pydiet.ingredients.ingredient import Ingredient
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

_UNITS_TEMPLATE = '''
    {qty}{units} of {ingredient_name} costs 
    £__.____
     ^^^^^^^

How much does {qty}{units} of {ingredient_name}
cost?
'''

class EditCostComponent(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self._igs:'ingredient_service' = inject('pydiet.ingredient_service')
        self._ies:'IngredientEditService' = inject('pydiet.cli.ingredient_edit_service')

    def print(self):
        # Build the output;
        output = _UNITS_TEMPLATE.format(\
            ingredient_name=self._ies.ingredient.name,
            qty=self._ies.temp_qty,
            units=self._ies.temp_qty_units
        )
        output = self.get_component('standard_page_component').print(output) + ' £'
        # Return it;
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
        # Catch qty data missing;
        if not self._ies.temp_qty or not self._ies.temp_qty_units:
            raise AttributeError
        # Set all the data;
        self._ies.ingredient.set_cost(
            cost, 
            self._ies.temp_qty, 
            self._ies.temp_qty_units)
        # Return to the menu;
        self.goto('..')