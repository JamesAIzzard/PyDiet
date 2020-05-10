from typing import TYPE_CHECKING, cast


from pinjector import inject
from pyconsoleapp.console_app_guard_component import ConsoleAppGuardComponent
from pyconsoleapp.builtin_components.yes_no_dialog_component import YesNoDialogComponent
from pydiet.ingredients.exceptions import DuplicateIngredientNameError

if TYPE_CHECKING:
    from pydiet.data import repository_service
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

class IngredientSaveCheckComponent(YesNoDialogComponent, ConsoleAppGuardComponent):

    def __init__(self):
        super().__init__()
        self._rp:'repository_service' = inject('pydiet.repository_service')
        self._ies:'IngredientEditService' = inject('pydiet.cli.ingredient_edit_service')
        self.message = 'Save changes to this ingredient?'

    def on_yes(self):
        # If the ingredient has a name;
        if self._ies.ingredient.name:
            # Go ahead and save;
            self._ies.save_changes()
            # Then remove the guard;
            self.clear_self()
        # If it isn't named;
        else:
            # Inform the user;
            self.app.info_message = 'Ingredient must be named before it can be saved.'
            # Clear the exit to the new page;
            self.clear_self()
            # Configure the exit guard for the edit page;
            self.app.guard_exit('home.ingredients.edit', 'IngredientSaveCheckComponent')
            # Redirect to edit page;
            self.app.goto('home.ingredients.edit')   

    def on_no(self):
        self.app.info_message = 'Ingredient not saved.'
        self.clear_self()