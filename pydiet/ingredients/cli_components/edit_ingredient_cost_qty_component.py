from pyconsoleapp import ConsoleAppComponent
from pyconsoleapp import parse_tools

from pydiet.ingredients import ingredient_edit_service as ies
from pydiet import units

_TEMPLATE = '''
    ____ of {ingredient_name} costs £__.____
    ^^^^ 

Enter the weight or volume, and units of {ingredient_name}
which you know the cost of.
(e.g 100g, or 1kg, 1L, etc.)

Valid units:
{valid_units}

'''


class EditIngredientCostQtyComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self._ies = ies.IngredientEditService()

    def run(self):
        # Zero the volume temp fields on ies;
        self._ies.temp_qty = None
        self._ies.temp_qty_units = None

    def print(self):
        output = _TEMPLATE.format(
            ingredient_name=self._ies.ingredient.name.lower(),
            valid_units=units.recognised_qty_units()
        )
        output = self.app.fetch_component('standard_page_component')\
            .call_print(output)
        return output

    def dynamic_response(self, response):
        # Try and parse the response as mass and units;
        try:
            qty, unit = parse_tools.parse_number_and_text(response)
        # Catch parse failure;
        except ValueError:
            self.app.error_message = "Unable to parse {} as a qty & unit. Try again."\
                .format(response)
            return
        # Parse unit to correct case;
        try:
            unit = units.parse_qty_unit(unit)
        # Catch unknown units;
        except units.UnknownUnitError:
            self.app.error_message = "{} is not a recognised unit.".format(unit)
            return            
        # Catch volume usage without density definition;
        if unit in units.recognised_vol_units() and \
            not self._ies.ingredient.density_is_defined:
            self.app.goto('home.ingredients.edit.set_density_question')
            return
        # Stash these values and move on to collect the cost;
        self._ies.temp_qty = qty
        self._ies.temp_qty_units = unit
        self.app.goto('home.ingredients.edit.cost')
