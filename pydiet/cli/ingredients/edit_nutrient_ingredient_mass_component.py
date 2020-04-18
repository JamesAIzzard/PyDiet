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

Enter the weight and units of the ingredient
you are referring to.
(e.g 100g or 1kg, etc.)
 '''

class EditNutrientIngredientMassComponent(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self._us:'utility_service' = inject('pydiet.utility_service')
        self._ies:'IngredientEditService' = inject('pydiet.cli.ingredient_edit_service')

    def print(self):
        output = _NUTRIENT_PER_MASS.format(
            ingredient_name=self._ies.ingredient.name,
            nutrient_name=self._ies.current_nutrient_amount.name
        )
        output = self.get_component('standard_page_component').print(output)
        return output

    def dynamic_response(self, response):
        # Try and parse the response as mass and units;
        try:
            mass_and_units = self._us.parse_number_and_units(response)
        except ValueError:
            self.app.error_message = "Unable to parse {} as a mass & unit. Try again."\
                .format(response)  
            return          
        # Set the values on the scope;  
        self._ies.temp_nutrient_ingredient_mass = mass_and_units[0]
        self._ies.temp_nutrient_ingredient_mass_units = mass_and_units[1]
        # Navigate to nutrient mass;
        self.goto('..edit_nutrient_mass')    