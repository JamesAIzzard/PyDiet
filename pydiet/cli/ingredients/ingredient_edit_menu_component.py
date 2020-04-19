from pydiet.configs import PRIMARY_NUTRIENTS
from typing import TYPE_CHECKING

from pinjector import inject

from pyconsoleapp import ConsoleAppComponent

if TYPE_CHECKING:
    from pydiet import configs
    from pydiet.ingredients import ingredient_service
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

_TEMPLATE = '''Ingredient Editor:
------------------

(s) -- Save Changes

(1) -- Edit Name: {name}

(2) -- Edit Cost: {cost}

(3) -- Configure Liquid Measurements: {density_status}

(4) -- Edit Flags:
{flags}
(5) -- Edit Nutrients:
{nutrients}
'''


class IngredientEditMenuComponent(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self._set_ingredient_name_message: str = 'Ingredient name must be set first.'
        self._cf: 'configs' = inject('pydiet.configs')
        self._igs: 'ingredient_service' = inject('pydiet.ingredient_service')
        self._ies: 'IngredientEditService' = inject(
            'pydiet.cli.ingredient_edit_service')
        self.set_option_response('1', self.on_edit_name)
        self.set_option_response('2', self.on_edit_cost)
        self.set_option_response('3', self.on_configure_liquid_measurements)
        self.set_option_response('4', self.on_edit_flags)
        self.set_option_response('5', self.on_edit_nutrients)

    def print(self):
        # Build the nutrient summary;
        n = '' # string for nutrient display
        for pn in self._cf.PRIMARY_NUTRIENTS:
            na = self._ies.ingredient.get_nutrient_amount(pn)
            n = n + '- {}\n'.format(self._igs.summarise_nutrient_amount(na))
        # Build the flag summary;
        f = ''
        for flag_name in self._ies.ingredient.all_flag_data.keys():
            f = f + '- {}\n'.format(self._igs.summarise_flag(
                self._ies.ingredient,
                flag_name
            ))
        # Assemble the template
        output = _TEMPLATE.format(
            name=self._igs.summarise_name(self._ies.ingredient),
            cost=self._igs.summarise_cost(self._ies.ingredient),
            density_status=self._igs.summarise_density(self._ies.ingredient),
            flags=f,
            nutrients=n
        )
        output = self.get_component('standard_page_component').print(output)
        return output

    def _check_name_defined(self) -> bool:
        if not self._ies.ingredient.name:
            self.app.error_message = self._set_ingredient_name_message
            return False
        else:
            return True

    def on_edit_name(self):
        self.goto('.edit_name')

    def on_edit_cost(self):
        if self._check_name_defined():
            self.goto('.edit_cost_mass')

    def on_configure_liquid_measurements(self):
        if self._check_name_defined():
            self.goto('.edit_density_volume')

    def on_edit_flags(self):
        ies: 'IngredientEditService' = inject(
            'pydiet.cli.ingredient_edit_service')
        if self._check_name_defined():
            if ies.ingredient.all_flags_undefined:
                self.goto('.flags.ask_cycle_flags')
            else:
                self.goto('.flags')

    def on_edit_nutrients(self) -> None:
        if self._check_name_defined():
            self.goto('.nutrients')
