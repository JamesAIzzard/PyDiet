from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent
from pinjector import inject

if TYPE_CHECKING:
    from pydiet import utility_service
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

_MASS_TEMPLATE = '''
    ____ of {ingredient_name} costs £__.____
    ^^^^ 

Enter the weight and units of {ingredient_name}
which you wish to value.
(e.g 100g, or 1kg, etc.)
'''


class EditCostMassComponent(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self._us:'utility_service' = inject(\
            'pydiet.utility_service')
        self._ies:'IngredientEditService' = inject('pydiet.cli.ingredient_edit_service')

    def print(self):
        output = _MASS_TEMPLATE.format(\
            ingredient_name=self._ies.ingredient.name)
        output = self.app.get_component('standard_page_component').print(output)
        return output

    def dynamic_response(self, response):
        # Try and parse the response as mass and units;
        try:
            mass_and_units = self._us.parse_number_and_units(response)
        # Catch parse failure;
        except ValueError:
            self.app.error_message = "Unable to parse {} as a mass & unit. Try again."\
                .format(response)
            return
        # Catch unrecognised unit failure;
        if not mass_and_units[1] in self._us.recognised_mass_units():
            self.app.error_message = "{} is not a recognised mass unit.".format(mass_and_units[1])
            return
        # Stash these values and move on to collect the cost;
        self._ies.temp_cost_mass = mass_and_units[0]
        self._ies.temp_cost_mass_units = mass_and_units[1]
        self.goto('..edit_cost')
