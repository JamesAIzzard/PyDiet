from pyconsoleapp import ConsoleAppComponent

from pydiet.shared.exceptions import UnknownUnitError
from pydiet.cli.ingredients import ingredient_edit_service as ies
from pydiet.shared import utility_service as uts

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
    def __init__(self, app):
        super().__init__(app)
        self._ies = ies.IngredientEditService()

    def print(self):
        output = _TEMPLATE.format(
            vol=self._ies.temp_qty,
            vol_units=self._ies.temp_qty_units,
            ingredient_name=self._ies.ingredient.name.lower(),
            valid_units=uts.recognised_mass_units()
        )
        output = self.app.fetch_component('standard_page_component').print(output)
        return output

    def dynamic_response(self, response):
        try:
            # Try and parse the number and text;
            mass, units = uts.parse_number_and_text(response)
        # Catch the parse failure;
        except ValueError:
            self.app.error_message = "Unable to parse {} as a mass and unit. Try again.".format(response)
            return
        try:
            # Try and parse the unit into the correct case;
            units = uts.parse_mass_unit(units)
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
