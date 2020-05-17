from typing import TYPE_CHECKING

from pinjector import inject
from pyconsoleapp.builtin_components.yes_no_dialog_component import YesNoDialogComponent

if TYPE_CHECKING:
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

class AskCycleIngredientFlagsComponent(YesNoDialogComponent):
    def __init__(self):
        super().__init__()
        self._ies:'IngredientEditService' = inject('pydiet.cli.ingredient_edit_service')
        self.message = 'Set all flags now?'

    def on_yes(self):
        self._ies.current_flag_number = 1
        self._ies.cycling_flags = True
        self.app.goto('home.ingredients.edit.flags.set_flag')

    def on_no(self):
        self.app.goto('home.ingredients.edit.flags')
