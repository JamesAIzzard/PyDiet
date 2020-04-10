from typing import TYPE_CHECKING

from pinjector import inject
from pyconsoleapp import ConsoleAppComponent

if TYPE_CHECKING:
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService
    from pydiet.ingredients import ingredient_service

_TEMPLATE = '''Nutrient Editor:
----------------

Primary Nutrients:
{primary_nutrients}

(n) -- Edit Other Nutrients
'''

class EditNutrientMenuComponent(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self._ies:'IngredientEditService' = inject('pydiet.cli.ingredient_edit_service')
        self._igs:'ingredient_service' = inject('pydiet.ingredient_service')
        self.set_option_response('n', self.on_edit_other)

    def print(self):
        pn = '' # primary nutrient string
        nmap = self._ies.primary_nutrient_number_name_map
        for option_number in nmap:
            na = self._ies.ingredient.get_nutrient_amount(nmap[option_number])
            pn = pn + '({}) -- {}\n'.format(
                option_number,
                self._igs.summarise_nutrient_amount(na)
            )
        output = _TEMPLATE.format(
            primary_nutrients=pn
        )
        output = self.get_component('standard_page_component').print(output)
        return output

    def on_edit_other(self):
        self.goto('..nutrient_search')