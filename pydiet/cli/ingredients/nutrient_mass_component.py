from typing import TYPE_CHECKING

from pinjector import inject
from pyconsoleapp import ConsoleAppComponent

if TYPE_CHECKING:
    from pydiet.utility_service import UtilityService
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

_NUTRIENT_MASS = '''
    In {mass_per}{mass_per_units} of {ingredient_name} there is

    ______ of {nutrient_name}
    ^^^^^^
Enter the weight and units of {nutrient_name}
present in {mass_per}{mass_per_units} of {ingredient_name}.
(e.g 100g or 1kg, etc.)
 '''

class NutrientMassComponent(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self._utility_service:'UtilityService' = inject('pydiet.utility_service')
        self._scope:'IngredientEditService' = inject('pydiet.ingredient_edit_service')

    def print(self):
        output = _NUTRIENT_MASS.format(
            ingredient_name = self._scope.ingredient.name,
            nutrient_name = self._scope.current_nutrient_name,
            mass_per = self._scope.temp_nutrient_mass_per,
            mass_per_units = self._scope.temp_nutrient_mass_per_units
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
        # Save the nutrient data to the ingredient;
        self._scope.ingredient.set_nutrient_data(
            self._scope.current_nutrient_name,
            mass_and_units[0], # mass value
            mass_and_units[1], # units value
            self._scope.temp_nutrient_mass_per,
            self._scope.temp_nutrient_mass_per_units
        )
        # Update the display;
        self._scope.show_ingredient_summary()
        # Navigate back to the nutrient menu;
        self.goto('..')
  