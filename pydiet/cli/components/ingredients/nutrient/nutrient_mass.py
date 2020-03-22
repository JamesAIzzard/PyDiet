from typing import TYPE_CHECKING
from pinjector import inject
from pyconsoleapp import ConsoleAppComponent
if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient
    from pydiet.utility_service import UtilityService
    from pydiet.ingredients.ingredient_service import IngredientService

_NUTRIENT_MASS = '''
    In {mass_per}{mass_per_units} of {ingredient_name} there is

    ______ of {nutrient_name}
    ^^^^^^
Enter the weight and units of {nutrient_name}
present in {mass_per}{mass_per_units} of {ingredient_name}.
(e.g 100g or 1kg, etc.)
 '''

class NutrientMass(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self.scope = self.get_scope('ingredient_edit')
        self.ingredient:'Ingredient' = self.scope.ingredient
        self._utility_service:'UtilityService' = inject('utility_service')
        self._ingredient_service:'IngredientService' = inject('ingredient_service')

    def print(self):
        scope = self.get_scope('ingredient_edit')
        output = _NUTRIENT_MASS.format(
            ingredient_name = scope.ingredient.name,
            nutrient_name = scope.get_nutrient_name(\
                scope.nutrient_number, scope),
            mass_per = scope.mass_per,
            mass_per_units = scope.mass_per_units
        )
        output = self.app.get_component('StandardPage').print(output)
        return output

    def dynamic_response(self, response):
        try:
            mass_and_units = self._utility_service.parse_mass_and_units(response)
            self.scope.mass = mass_and_units[0]
            self.scope.mass_units = mass_and_units[1]
            # Save the nutrient data to the ingredient;
            self.ingredient.set_nutrient_data(
                self.scope.get_nutrient_name(self.scope.nutrient_number, self.scope),
                self.scope.mass,
                self.scope.mass_units,
                self.scope.mass_per,
                self.scope.mass_per_units
            )
            # Update the display;
            self.app.set_window_text(
                self._ingredient_service.summarise_ingredient(
                    self.ingredient
                )
            )
            self.app.show_text_window()
            # Navigate back to the nutrient menu;
            self.app.navigate_back()
        except ValueError:
            self.app.error_message = "Unable to parse {} as a mass & unit. Try again."\
                .format(response)     