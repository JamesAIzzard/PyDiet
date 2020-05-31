from pyconsoleapp import ConsoleAppGuardComponent
from pyconsoleapp.builtin_components.yes_no_dialog_component import YesNoDialogComponent

from pydiet.recipes.exceptions import (
    RecipeNameUndefinedError
)
from pydiet.cli.recipes import recipe_edit_service as res

class RecipeSaveCheckComponent(YesNoDialogComponent, ConsoleAppGuardComponent):

    def __init__(self, app):
        super().__init__(app)
        self._res = res.RecipeEditService()
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