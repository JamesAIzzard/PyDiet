from typing import TYPE_CHECKING

from pinjector import inject
from pyconsoleapp import ConsoleAppComponent

from pydiet.ingredients.ingredient import (
    ConstituentsExceedGroupError,
    NutrientQtyExceedsIngredientQtyError
)

if TYPE_CHECKING:
    from pydiet import utility_service
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

_NUTRIENT_MASS = '''
    In {mass_per}{mass_per_units} of {ingredient_name} there is

    ______ of {nutrient_name}
    ^^^^^^
Enter the weight and units of {nutrient_name}
present in {mass_per}{mass_per_units} of {ingredient_name}.
(e.g 100g or 1kg, etc.)
 '''

class EditNutrientMassComponent(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self._us:'utility_service' = inject('pydiet.utility_service')
        self._ies:'IngredientEditService' = inject('pydiet.cli.ingredient_edit_service')

    def print(self):
        output = _NUTRIENT_MASS.format(
            ingredient_name = self._ies.ingredient.name,
            nutrient_name = self._ies.current_nutrient_amount.name,
            mass_per = self._ies.temp_nutrient_ingredient_mass,
            mass_per_units = self._ies.temp_nutrient_ingredient_mass_units
        )
        output = self.get_component('standard_page_component').print(output)
        return output

    def dynamic_response(self, response):
        # Try and parse the response as mass and units;
        try:
            mass_and_units = self._us.parse_mass_and_units(response)
        except ValueError:
            self.app.error_message = "Unable to parse {} as a mass & unit. Try again."\
                .format(response)
            return
        # Try the nutrient data to the ingredient;
        try:
            self._ies.ingredient.set_nutrient_amount(
                self._ies.current_nutrient_amount.name,
                self._ies.temp_nutrient_ingredient_mass,
                self._ies.temp_nutrient_ingredient_mass_units,
                mass_and_units[0], # mass value
                mass_and_units[1] # units value
            )
        except (ConstituentsExceedGroupError, NutrientQtyExceedsIngredientQtyError) as err:
            self.app.error_message = (str(err))
            return
        # Navigate back to the nutrient menu;
        self.goto('..')
  