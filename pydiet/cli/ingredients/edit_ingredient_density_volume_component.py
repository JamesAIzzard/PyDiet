from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent
from pinjector import inject

from pydiet.shared.exceptions import UnknownUnitError

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

Valid units:
{valid_units}

'''

class EditIngredientDensityVolumeComponent(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self._ies:'IngredientEditService' = inject('pydiet.cli.ingredient_edit_service')
        self._us:'utility_service' = inject('pydiet.utility_service')

    def print(self):
        output = _TEMPLATE.format(
            ingredient_name=self._ies.ingredient.name.lower(),
            valid_units=self._us.recognised_vol_units()
        )
        output = self.app.fetch_component('standard_page_component').print(output)
        return output

    def dynamic_response(self, response):
        # Try and parse the response as mass and units;
        try:
            vol, units = self._us.parse_number_and_text(response)
        # Catch parse failure;
        except ValueError:
            self.app.error_message = "Unable to parse {} as a volume & unit. Try again."\
                .format(response)
            return
        # Parse unit to correct case;
        try:
            units = self._us.parse_vol_unit(units)
        # Catch unknown units;
        except UnknownUnitError:
            self.app.error_message = "{} is not a recognised unit of volume.".format(units)
            return  
        # Stash these values and move on to collect the weight;
        self._ies.temp_qty = vol
        self._ies.temp_qty_units = units
        # Head on to collect the mass;
        self.app.goto('..edit_density_mass')