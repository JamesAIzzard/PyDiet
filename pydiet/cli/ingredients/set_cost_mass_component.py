from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent
from pinjector import inject

if TYPE_CHECKING:
    from pydiet.utility_service import UtilityService
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

_MASS_TEMPLATE = '''
    ____ of {ingredient_name} costs £__.____
    ^^^^ 

Enter the weight and units of {ingredient_name}
which you wish to value.
(e.g 100g, or 1kg, etc.)
'''


class SetCostMassComponent(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self._utility_service:'UtilityService' = inject(\
            'pydiet.utility_service')
        self._scope:'IngredientEditService' = inject('pydiet.cli.ingredient_edit_service')

    def print(self):
        output = _MASS_TEMPLATE.format(\
            ingredient_name=self._scope.ingredient.name)
        output = self.app.get_component('standard_page_component').print(output)
        return output

    def dynamic_response(self, response):
        # Try and parse the response as mass and units;
        mass_and_units = None
        try:
            mass_and_units = self._utility_service.parse_mass_and_units(response)
        except ValueError:
            self.app.error_message = "Unable to parse {} as a mass & unit. Try again."\
                .format(response)
            return
        # Stash these values and move on to collect the cost;
        self._scope.temp_cost_mass = mass_and_units[0]
        self._scope.temp_cost_mass_units = mass_and_units[1]
        self.goto('..cost')
