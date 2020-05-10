from typing import TYPE_CHECKING

from pyconsoleapp.builtin_components.yes_no_dialog_component import YesNoDialogComponent
from pinjector import inject


if TYPE_CHECKING:
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService
    from pydiet.data import repository_service

class ConfirmIngredientDeleteComponent(YesNoDialogComponent):

    def __init__(self):
        super().__init__()
        self._ies:'IngredientEditService' = inject('pydiet.cli.ingredient_edit_service')
        self._rp:'repository_service' = inject('pydiet.repository_service')
        self.message = 'Are you sure you want to delete {}'.format(
            self._ies.ingredient.name
        )

    def on_yes(self):
        # If no datafile;
        if not self._ies.datafile_name:
            raise AttributeError
        # Delete the datafile;
        self._rp.delete_ingredient_data(self._ies.datafile_name)
        # Set status message;
        self.app.info_message = '{} deleted.'.format(self._ies.ingredient.name)
        # Redirect;
        self.app.goto('home.ingredients')

    def on_no(self):
        self.app.info_message = 'Ingredient was not deleted.'
        self.app.goto('home.ingredients')