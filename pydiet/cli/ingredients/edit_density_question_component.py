from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent
from pinjector import inject

if TYPE_CHECKING:
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

_TEMPLATE = '''Volumetric measurements are not configured 
on {ingredient_name} yet. Would you like to configure
them now?

    (y)es/(n)o

'''


class EditDensityQuestionComponent(ConsoleAppComponent):
    def __init__(self):
        super().__init__()
        self._ies: 'IngredientEditService' = inject(
            'pydiet.cli.ingredient_edit_service')
        self.set_option_response('y', self.on_yes)
        self.set_option_response('n', self.on_no)

    def print(self):
        output = _TEMPLATE.format(
            ingredient_name=self._ies.ingredient.name
        )
        output = self.get_component('standard_page_component')\
            .print(output)
        return output

    def on_yes(self):
        self.goto('..edit_density_volume')

    def on_no(self):
        self.goto('..')