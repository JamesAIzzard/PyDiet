from typing import TYPE_CHECKING, cast

from pyconsoleapp import ConsoleAppComponent
from pinjector import inject

if TYPE_CHECKING:
    from pydiet.ingredients import ingredient_service
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService
    from pydiet.cli.ingredients.ingredient_save_check_component import IngredientSaveCheckComponent

_MENU_TEMPLATE = '''Choose an option:
(1) -- Create a new ingredient.
(2) -- Edit an existing ingredient.
(3) -- Delete an existing ingredient.
(4) -- View ingredients.
'''


class IngredientMenuComponent(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self._ies:'IngredientEditService' = inject('pydiet.cli.ingredient_edit_service')
        self._igs:'ingredient_service' = inject('pydiet.ingredient_service')
        self.set_option_response('1', self.on_create)
        self.set_option_response('2', self.on_edit)
        self.set_option_response('3', self.on_delete)
        self.set_option_response('4', self.on_view)

    def run(self):
        self._ies.ingredient = None
        self._ies.datafile_name = None

    def print(self):
        output = _MENU_TEMPLATE
        output = self.app.get_component('standard_page_component').print(output)
        return output

    def on_create(self):
        # Put a fresh ingredient on the scope;
        self._ies.ingredient = self._igs.load_new_ingredient()
        # Configure the save reminder;
        cast(
            'IngredientSaveCheckComponent', 
            self.get_component('ingredient_save_check_component')
        ).guarded_route = 'home.ingredients.new'
        self.guard_exit('home.ingredients.new', 'ingredient_save_check_component')
        # Go;
        self.goto('.new')

    def on_edit(self):
        self.goto('home.ingredients.edit.search')

    def on_delete(self):
        self.goto('home.ingredients.delete.search')

    def on_view(self):
        self.goto('home.ingredients.view')
