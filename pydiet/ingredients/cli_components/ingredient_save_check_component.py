from typing import TYPE_CHECKING

import pyconsoleapp as pcap

from pydiet import ingredients

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient

class IngredientSaveCheckComponent(
    pcap.builtin_components.yes_no_dialog_component.YesNoDialogComponent,
    pcap.ConsoleAppGuardComponent):
    
    def __init__(self, app):
        super().__init__(app)
        self.message = 'Save changes to this ingredient?'
        self.ingredient:'Ingredient'

    def on_yes(self):
        raise NotImplementedError

    def on_no(self):
        raise NotImplementedError
