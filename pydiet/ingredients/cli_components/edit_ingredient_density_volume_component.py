from pyconsoleapp import ConsoleAppComponent
from pyconsoleapp import parse_tools

from pydiet import units
from pydiet.ingredients import ingredient_edit_service as igs

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
    def __init__(self, app):
        super().__init__(app)
        self._ies = igs.IngredientEditService()

    def print(self):
        output = _TEMPLATE.format(
            ingredient_name=self._ies.ingredient.name.lower(),
            valid_units=units.recognised_vol_units()
        )
        output = self.app.fetch_component('standard_page_component').print(output)
        return output

    def dynamic_response(self, response):
        # Try and parse the response as mass and units;
        try:
            vol, unit = parse_tools.parse_number_and_text(response)
        # Catch parse failure;
        except ValueError:
            self.app.error_message = "Unable to parse {} as a volume & unit. Try again."\
                .format(response)
            return
        # Parse unit to correct case;
        try:
            unit = units.parse_vol_unit(unit)
        # Catch unknown units;
        except units.UnknownUnitError:
            self.app.error_message = "{} is not a recognised unit of volume.".format(unit)
            return  
        # Stash these values and move on to collect the weight;
        self._ies.temp_qty = vol
        self._ies.temp_qty_units = unit
        # Head on to collect the mass;
        self.app.goto('home.ingredients.edit.density_mass')