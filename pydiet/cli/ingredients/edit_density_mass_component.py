from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent
from pinjector import inject

if TYPE_CHECKING:
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService
    from pydiet import utility_service

_TEMPLATE = '''
    {vol}{vol_units} of {ingredient_name}
    
    weighs ______
           ^^^^^^
Enter the mass of {vol}{vol_units} of {ingredient_name}.
(e.g 100g, or 1kg, etc.)
'''

class EditDensityMassComponent(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self._ies:'IngredientEditService' = inject('pydiet.cli.ingredient_edit_service')
        self._us:'utility_service' = inject('pydiet.utility_service')

    def print(self):
        output = _TEMPLATE.format(
            vol=self._ies.temp_volume,
            vol_units=self._ies.temp_volume_units,
            ingredient_name=self._ies.ingredient.name
        )
        output = self.get_component('standard_page_component').print(output)
        return output

    def dynamic_response(self, response):
        # Try and parse the mass and units;
        try:
            mass_and_units = self._us.parse_number_and_units(response)
        # Catch the parse failure;
        except ValueError:
            self.app.error_message = "Unable to parse {} as a mass and unit. Try again.".format(response)
            return
        # Catch the unrecongnised unit;
        if not mass_and_units[1] in self._us.recognised_mass_units():
            self.app.error_message = "{} is not a recognised mass unit.".format(mass_and_units[1])
            return
        # Go ahead and define the ingredient density;
        self._ies.ingredient.set_density(
            self._ies.temp_volume,
            self._ies.temp_volume_units,
            mass_and_units[0], # mass per volume
            mass_and_units[1] # mass units per volume
        )
