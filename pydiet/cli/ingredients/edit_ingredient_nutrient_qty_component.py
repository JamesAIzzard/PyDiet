from typing import TYPE_CHECKING

from pinjector import inject
from pyconsoleapp import ConsoleAppComponent

from pydiet.shared.exceptions import UnknownUnitError

if TYPE_CHECKING:
    from pydiet.shared import utility_service
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

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
    def __init__(self):
        super().__init__()
        self._us:'utility_service' = inject('pydiet.utility_service')
        self._ies:'IngredientEditService' = inject('pydiet.cli.ingredient_edit_service')

    def print(self):
        output = _NUTRIENT_PER_MASS.format(
            ingredient_name=self._ies.ingredient.name.lower(),
            nutrient_name=self._ies.current_nutrient_amount.name,
            valid_units=self._us.recognised_qty_units()
        )
        output = self.app.fetch_component('standard_page_component').print(output)
        return output

    def dynamic_response(self, response):
        # Try and parse the response as mass and units;
        try:
            qty, units = self._us.parse_number_and_text(response)
        # Catch parse failure;
        except ValueError:
            self.app.error_message = "Unable to parse {} as a qty & unit. Try again."\
                .format(response)
            return
        # Parse unit to correct case;
        try:
            units = self._us.parse_qty_unit(units)
        # Catch unknown units;
        except UnknownUnitError:
            self.app.error_message = "{} is not a recognised unit.".format(units)
            return   
        # Catch volume usage without density definition;
        if units in self._us.recognised_vol_units() and \
            not self._ies.ingredient.density_is_defined:
            self.app.goto('...edit_density_question')
            return      
        # Set the values on the scope;  
        self._ies.temp_qty = qty
        self._ies.temp_qty_units = units
        # Navigate to nutrient mass;
        self.app.goto('..edit_nutrient_mass')    