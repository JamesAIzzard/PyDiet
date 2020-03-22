from typing import TYPE_CHECKING
from pyconsoleapp import ConsoleAppComponent
from pinjector import inject
if TYPE_CHECKING:
    from pydiet.ingredients.ingredient_service import IngredientService
    from pydiet.ingredients.ingredient import Ingredient

_UNITS_TEMPLATE = '''
    {mass}{units} of {ingredient_name} costs £__.____
                {spacer}^^^^^^^

How much does {mass}{units} of {ingredient_name}
cost?
'''

class SetCost(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self._ingredient_service:'IngredientService' = inject('ingredient_service')

    def print(self):
        scope = self.get_scope('ingredient_edit')
        output = _UNITS_TEMPLATE.format(\
            ingredient_name=scope.ingredient.name,
            mass=scope.cost_mass,
            units=scope.cost_mass_units,
            spacer=' '*len(scope.ingredient.name+\
                str(scope.cost_mass)+scope.cost_mass_units)
        )
        output = self.app.get_component('StandardPage').print(output)
        return output

    def dynamic_response(self, response):
        scope = self.get_scope('ingredient_edit')
        try:
            scope.cost = float(response)
            ingredient:'Ingredient' = scope.ingredient
            ingredient.set_cost(scope.cost, scope.cost_mass, scope.cost_mass_units)
            self.app.info_message = 'Cost set successfully.'
            self.app.set_window_text(self._ingredient_service.\
                summarise_ingredient(ingredient))
            self.app.navigate_back()
        except ValueError:
            self.app.error_message = "Unable to parse {} as a cost. Try again."\
                .format(response)