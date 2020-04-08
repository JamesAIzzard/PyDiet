from typing import TYPE_CHECKING

from pinjector import inject

from pyconsoleapp import ConsoleAppComponent

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient
    from pydiet.ingredients import ingredient_service
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

_TEMPLATE = '''Ingredient Editor:
(s) -- Save Changes.

(1) -- Edit Name: {name}

(2) -- Edit Cost: {cost}

(3) -- Edit Flags
{flags}

(4) -- Edit Nutrients:
{nutrients}
'''


class IngredientEditMenuComponent(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self._set_ingredient_name_message: str = 'Ingredient name must be set first.'
        self.set_option_response('1', self.on_edit_name)
        self.set_option_response('2', self.on_edit_cost)
        self.set_option_response('3', self.on_edit_flags)
        self.set_option_response('4', self.on_edit_nutrients)

    def print(self):
        igs: 'ingredient_service' = inject('pydiet.ingredient_service')
        ies: 'IngredientEditService' = inject('pydiet.cli.ingredient_edit_service')
        output = _TEMPLATE.format(
            name=igs.summarise_name(ies.ingredient),
            cost=igs.summarise_cost(ies.ingredient),
            flags=igs.summarise_flags(ies.ingredient),
            nutrients=igs.summarise_primary_nutrients(ies.ingredient)
        )
        output = self.get_component('standard_page_component').print(output)
        return output

    def _check_name_defined(self) -> bool:
        if not self._scope.ingredient.name:
            self.app.error_message = self._set_ingredient_name_message
            return False
        else:
            return True

    def on_edit_name(self):
        self.goto('.name')

    def on_edit_cost(self):
        self.goto('.cost_mass')

    def on_edit_flags(self):
        if self._check_name_defined():
            if self._scope.ingredient.all_flags_undefined:
                self.goto('.flags.set_all?')
            else:
                self.goto('.flags')

    def on_edit_nutrients(self, group_name: str) -> None:
        if self._check_name_defined():
            self.goto('.nutrient_search')
