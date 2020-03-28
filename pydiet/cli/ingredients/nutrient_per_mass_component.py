from typing import TYPE_CHECKING

from pinjector import inject
from pyconsoleapp import ConsoleAppComponent

if TYPE_CHECKING:
    from pydiet.utility_service import UtilityService
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

_NUTRIENT_PER_MASS = '''
    In _____ of {ingredient_name} there is
       ^^^^^
    ______ of {nutrient_name}.

Enter the weight and units of the ingredient
you are referring to.
(e.g 100g or 1kg, etc.)
 '''

class NutrientPerMassComponent(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self._utility_service:'UtilityService' = inject('pydiet.utility_service')
        self._scope:'IngredientEditService' = inject('pydiet.ingredient_edit_service')

    def print(self):
        output = _NUTRIENT_PER_MASS.format(
            ingredient_name = self._scope.ingredient.name,
            nutrient_name = self._scope.current_nutrient_name
        )
        output = self.get_component('StandardPageComponent').print(output)
        return output

    def dynamic_response(self, response):
        # Try and parse the response as mass and units;
        try:
            mass_and_units = self._utility_service.parse_mass_and_units(response)
        except ValueError:
            self.app.error_message = "Unable to parse {} as a mass & unit. Try again."\
                .format(response)  
            return          
        # Set the values on the scope;  
        self._scope.temp_nutrient_mass_per = mass_and_units[0]
        self._scope.temp_nutrient_mass_per_units = mass_and_units[1]
        # Navigate to nutrient mass;
        self.goto('..nutrient_mass')    