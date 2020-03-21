from typing import TYPE_CHECKING
from pyconsoleapp import ConsoleAppComponent
from pinjector import inject
if TYPE_CHECKING:
    from pydiet.ingredients.ingredient_service import IngredientService
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
        self._ingredient_service: 'IngredientService' = inject(
            'ingredient_service')
        self.scope = self.get_scope('ingredient_edit')
        self.ingredient:'Ingredient' = self.scope.ingredient

    def print(self):
        output = _MASS_TEMPLATE.format(\
            ingredient_name=self.ingredient.name)
        output = self.app.get_component('StandardPage').print(output)
        return output

    def dynamic_response(self, response):
        pass
