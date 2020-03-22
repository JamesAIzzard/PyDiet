from typing import TYPE_CHECKING
from pyconsoleapp import ConsoleAppComponent
from pinjector import inject
if TYPE_CHECKING:
    from pydiet.ingredients.ingredient_service import IngredientService
    from pydiet.utility_service import UtilityService
    from pydiet.ingredients.ingredient import Ingredient

_MASS_TEMPLATE = '''
    ____ of {ingredient_name} costs £__.____
    ^^^^ 

Enter the weight and units of {ingredient_name}
which you wish to value. 
(e.g 100g, or 1kg, etc.)

>>> '''


class SetCostMass(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self._ingredient_service: 'IngredientService' = inject(\
            'ingredient_service')
        self._utility_service:'UtilityService' = inject(\
            'utility_service')
        self.scope = self.get_scope('ingredient_edit')
        self.ingredient:'Ingredient' = self.scope.ingredient

    def print(self):
        output = _MASS_TEMPLATE.format(\
            ingredient_name=self.ingredient.name)
        output = self.app.get_component('StandardPage').print(output)
        return output

    def dynamic_response(self, response):
        try:
            mass_and_units = self._utility_service.parse_mass_and_units(response)
            self.scope.cost_mass = mass_and_units[0]
            self.scope.cost_mass_units = mass_and_units[1]
            self.app.navigate_back()
            self.app.navigate(['.', 'cost'])
        except ValueError:
            self.app.error_message = "Unable to parse {} as a mass & unit. Try again."\
                .format(response)
