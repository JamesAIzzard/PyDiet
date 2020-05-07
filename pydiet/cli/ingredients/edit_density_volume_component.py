from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent
from pinjector import inject

if TYPE_CHECKING:
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService
    from pydiet.shared import utility_service

_TEMPLATE = '''
    ______ of {ingredient_name}
    ^^^^^^
    weighs ______

Enter the volume of the ingredient
you wish to define the weight for.
(e.g 1L, 1tsp, 1tbsp, 1cm3 or 1m3)
'''

class EditDensityVolumeComponent(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self._ies:'IngredientEditService' = inject('pydiet.cli.ingredient_edit_service')
        self._us:'utility_service' = inject('pydiet.utility_service')

    def print(self):
        output = _TEMPLATE.format(
            ingredient_name=self._ies.ingredient.name
        )
        output = self.app.get_component('standard_page_component').print(output)
        return output

    def dynamic_response(self, response):
        # Lowercase the response, since all vols are lowercase;
        response = response.lower()
        # Try and parse the volume and units from what was entered;
        try:
            vol_and_units = self._us.parse_number_and_units(response)
        # Catch general parse failure;
        except ValueError:
            self.app.error_message = "Unable to parse {} as a volume and unit. Try again.".format(response)
            return
        # Catch unrecognised unit;
        if not vol_and_units[1] in self._us.recognised_vol_units():
            self.app.error_message = "{} is not a recognised vol unit.".format(vol_and_units[1])
            return
        # Stash these values and move on to collect the weight;
        self._ies.temp_qty = vol_and_units[0]
        self._ies.temp_qty_units = vol_and_units[1]
        # Head on to collect the mass;
        self.goto('..edit_density_mass')