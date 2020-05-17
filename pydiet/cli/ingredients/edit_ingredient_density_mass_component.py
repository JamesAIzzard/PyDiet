from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent
from pinjector import inject

from pydiet.shared.exceptions import UnknownUnitError

if TYPE_CHECKING:
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService
    from pydiet.shared import utility_service

_TEMPLATE = '''
    {vol}{vol_units} of {ingredient_name}
    
    weighs ______
           ^^^^^^
Enter the mass of {vol}{vol_units} of {ingredient_name}.
(e.g 100g, or 1kg, etc.)

Valid units:
{valid_units}

'''

class EditIngredientDensityMassComponent(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self._ies:'IngredientEditService' = inject('pydiet.cli.ingredient_edit_service')
        self._us:'utility_service' = inject('pydiet.utility_service')

    def print(self):
        output = _TEMPLATE.format(
            vol=self._ies.temp_qty,
            vol_units=self._ies.temp_qty_units,
            ingredient_name=self._ies.ingredient.name.lower(),
            valid_units=self._us.recognised_mass_units()
        )
        output = self.app.fetch_component('standard_page_component').print(output)
        return output

    def dynamic_response(self, response):
        try:
            # Try and parse the number and text;
            mass, units = self._us.parse_number_and_text(response)
        # Catch the parse failure;
        except ValueError:
            self.app.error_message = "Unable to parse {} as a mass and unit. Try again.".format(response)
            return
        try:
            # Try and parse the unit into the correct case;
            units = self._us.parse_mass_unit(units)
        except UnknownUnitError:
            self.app.error_message = "{} is not a recognised mass unit.".format(units)
            return            
        # Go ahead and define the ingredient density;
        if self._ies.temp_qty and self._ies.temp_qty_units:
            self._ies.ingredient.set_density(
                self._ies.temp_qty,
                self._ies.temp_qty_units,
                mass,
                units
            )
        else:
            raise AttributeError
        # Done, head back to edit menu;
        self.app.goto('home.ingredients.edit')
