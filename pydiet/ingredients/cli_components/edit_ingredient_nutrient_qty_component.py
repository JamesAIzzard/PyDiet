from pyconsoleapp import ConsoleAppComponent, parse_tools

from pydiet import units
from pydiet.ingredients import ingredient_edit_service as ies

_NUTRIENT_PER_MASS = '''
    In _____ of {ingredient_name} there is
       ^^^^^
    ______ of {nutrient_name}.

Enter the weight or volume, and units of the ingredient
you are referring to.
(e.g 100g or 1kg, 100ml, 2L etc.)

Valid units:
{valid_units}

 '''

class EditIngredientNutrientQtyComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self._ies = ies.IngredientEditService()

    def print(self):
        output = _NUTRIENT_PER_MASS.format(
            ingredient_name=self._ies.ingredient.name.lower(),
            nutrient_name=self._ies.current_nutrient_amount.name,
            valid_units=units.recognised_qty_units()
        )
        output = self.app.fetch_component('standard_page_component').call_print(output)
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
        # Set the values on the scope;  
        self._ies.temp_qty = qty
        self._ies.temp_qty_units = unit
        # Navigate to nutrient mass;
        self.app.goto('home.ingredients.edit.nutrients.nutrient_mass')    