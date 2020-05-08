from typing import TYPE_CHECKING, cast

from pinjector import inject

from pyconsoleapp.builtin_components.yes_no_dialog_component import YesNoDialogComponent
from pydiet.ingredients.exceptions import DuplicateIngredientNameError

if TYPE_CHECKING:
    from pydiet.data import repository_service
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

class IngredientSaveCheckComponent(YesNoDialogComponent):

    def __init__(self):
        super().__init__()
        self._rp:'repository_service' = inject('pydiet.repository_service')
        self._ies:'IngredientEditService' = inject('pydiet.cli.ingredient_edit_service')
        self.set_option_response('y', self.on_yes_save)
        self.set_option_response('n', self.on_no_dont_save)
        self.message:str = 'Save changes to this ingredient?'
        self.guarded_route:str

    def on_yes_save(self):
        # If the ingredient has a name;
        if self._ies.ingredient.name:
            # Go ahead and save;
            self._ies.save_changes()
            # Then remove the guard;
            self.app.clear_exit(self.guarded_route)
        # If it isn't named;
        else:
            # Inform the user;
            self.app.info_message = 'Ingredient must be named before it can be saved.'
            # Clear the exit to the new page;
            self.app.clear_exit(self.guarded_route)
            # Configure the exit guard for the edit page;
            self.app.guard_exit('home.ingredients.edit', 'ingredient_save_check_component')
            cast(
                'IngredientSaveCheckComponent',
                self.get_component('ingredient_save_check_component')
            ).guarded_route = 'home.ingredients.edit'
            # Redirect to edit page;
            self.goto('home.ingredients.edit')   

    def on_no_dont_save(self):
        self.app.info_message = 'Ingredient not saved.'
        self.app.clear_exit(self.guarded_route)     