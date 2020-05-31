from pyconsoleapp.builtin_components.yes_no_dialog_component import YesNoDialogComponent

from pydiet.ingredients import ingredient_edit_service as ies

class AskCycleIngredientFlagsComponent(YesNoDialogComponent):
    def __init__(self, app):
        super().__init__(app)
        self._ies = ies.IngredientEditService()
        self.message = 'Set all flags now?'

    def on_yes(self):
        self._ies.current_flag_number = 1
        self._ies.cycling_flags = True
        self.app.goto('home.ingredients.edit.flags.set_flag')

    def on_no(self):
        self.app.goto('home.ingredients.edit.flags')
