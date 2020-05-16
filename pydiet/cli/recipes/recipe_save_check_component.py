from typing import TYPE_CHECKING


from pinjector import inject
from pyconsoleapp.console_app_guard_component import ConsoleAppGuardComponent
from pyconsoleapp.builtin_components.yes_no_dialog_component import YesNoDialogComponent

from pydiet.recipes.exceptions import (
    RecipeNameUndefinedError
)

if TYPE_CHECKING:
    from pydiet.data import repository_service
    from pydiet.cli.recipes.recipe_edit_service import RecipeEditService

class RecipeSaveCheckComponent(YesNoDialogComponent, ConsoleAppGuardComponent):

    def __init__(self):
        super().__init__()
        self._rp:'repository_service' = inject('pydiet.repository_service')
        self._res:'RecipeEditService' = inject('pydiet.cli.recipe_edit_service')
        self.message = 'Save changes to this recipe?'

    def on_yes(self):
        # Try and save;
        try:
            # Perform the save;
            self._res.save_changes()
            # Clear the exit guard;
            self.clear_self()
        # If the recipe was unnamed;
        except RecipeNameUndefinedError:
            # Tell the user;
            self.app.info_message = 'Recipe must be named before it can be saved.'
            # Reverse;
            self.app.back()

    def on_no(self):
        # Confirm;
        self.app.info_message = 'Recipe not saved.'
        # Clear the exit guard;
        self.clear_self()