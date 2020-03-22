from typing import TYPE_CHECKING
from pinjector import inject
from pyconsoleapp import ConsoleAppComponent
if TYPE_CHECKING:
    from pydiet.utility_service import UtilityService

_NUTRIENT_PER_MASS = '''
    In _____ of {ingredient_name} there is
       ^^^^^
    ______ of {nutrient_name}.

Enter the weight and units of the ingredient
you are referring to.
(e.g 100g or 1kg, etc.)
 '''

class NutrientPerMass(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self._utility_service:'UtilityService' = inject('utility_service')
        self.scope = self.get_scope('ingredient_edit')

    def print(self):
        scope = self.get_scope('ingredient_edit')
        output = _NUTRIENT_PER_MASS.format(
            ingredient_name = scope.ingredient.name,
            nutrient_name = scope.get_nutrient_name(
                scope.nutrient_number, scope
            )
        )
        output = self.app.get_component('StandardPage').print(output)
        return output

    def dynamic_response(self, response):
        try:
            mass_and_units = self._utility_service.parse_mass_and_units(response)
            self.scope.mass_per = mass_and_units[0]
            self.scope.mass_per_units = mass_and_units[1]
            # Navigate to nutrient mass;
            self.app.navigate_back()
            self.app.navigate(['.', 'nutrient_mass'])
        except ValueError:
            self.app.error_message = "Unable to parse {} as a mass & unit. Try again."\
                .format(response)        