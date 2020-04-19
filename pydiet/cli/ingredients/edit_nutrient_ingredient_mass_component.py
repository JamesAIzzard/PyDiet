from typing import TYPE_CHECKING

from pinjector import inject
from pyconsoleapp import ConsoleAppComponent

if TYPE_CHECKING:
    from pydiet import utility_service
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

_NUTRIENT_PER_MASS = '''
    In _____ of {ingredient_name} there is
       ^^^^^
    ______ of {nutrient_name}.

Enter the weight or volume, and units of the ingredient
you are referring to.
(e.g 100g or 1kg, 100ml, 2L etc.)
 '''

class EditNutrientIngredientMassComponent(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self._us:'utility_service' = inject('pydiet.utility_service')
        self._ies:'IngredientEditService' = inject('pydiet.cli.ingredient_edit_service')

    def run(self):
        # Zero the volume temp fields on ies;
        self._ies.temp_volume = None
        self._ies.temp_volume_units = None

    def print(self):
        output = _NUTRIENT_PER_MASS.format(
            ingredient_name=self._ies.ingredient.name,
            nutrient_name=self._ies.current_nutrient_amount.name
        )
        output = self.get_component('standard_page_component').print(output)
        return output

    def dynamic_response(self, response):
        # Lowercase the response;
        response = response.lower()
        # Try and parse the response as mass and units;
        try:
            qty_and_units = self._us.parse_number_and_units(response)
        except ValueError:
            self.app.error_message = "Unable to parse {} as a mass & unit. Try again."\
                .format(response)  
            return      
        # Split the qty & units out;
        qty = qty_and_units[0]
        units = qty_and_units[1]   
        # Catch volume usage without density definition;
        if units in self._us.recognised_vol_units() and \
            not self._ies.ingredient.density_is_defined:
            self.goto('...edit_density_question')
            return
        # Catch unrecognised unit failure;
        if not units in self._us.recognised_mass_units() and \
            not units in self._us.recognised_vol_units():
            self.app.error_message = "{} is not a recognised unit.".format(units)
            return
        # If we are defining by volume;
        if units in self._us.recognised_vol_units():
            # Stash the volume and units for use in the next template;
            self._ies.temp_volume = qty
            self._ies.temp_volume_units = units
            # Use the density to get the mass in g for the given volume;
            qty = self._ies.ingredient.convert_vol_to_grams(qty, units)
            units = 'g'         
        # Set the values on the scope;  
        self._ies.temp_nutrient_ingredient_mass = qty
        self._ies.temp_nutrient_ingredient_mass_units = units
        # Navigate to nutrient mass;
        self.goto('..edit_nutrient_mass')    