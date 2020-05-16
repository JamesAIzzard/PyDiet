from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent
from pinjector import inject

if TYPE_CHECKING:
    from pydiet.recipes import recipe_service
    from pydiet.cli.recipes.recipe_edit_service import RecipeEditService
#   from pydiet.cli.recipes.recipe_save_check_component import RecipeSaveCheckComponent

_MENU_TEMPLATE = '''Choose an option:
(1) -- Create a new recipe.
(2) -- Edit an existing recipe.
(3) -- Delete an existing recipe.
(4) -- View recipes.
'''


class RecipeMenuComponent(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self._res: 'RecipeEditService' = inject(
            'pydiet.cli.recipe_edit_service')
        self._rcs: 'recipe_service' = inject('pydiet.recipe_service')
        self.set_option_response('1', self.on_create)
        self.set_option_response('2', self.on_edit)
        self.set_option_response('3', self.on_delete)
        self.set_option_response('4', self.on_view)

    def run(self):
        self._res.recipe = None
        self._res.datafile_name = None

    def print(self):
        output = _MENU_TEMPLATE
        output = self.app.fetch_component(
            'standard_page_component').print(output)
        return output

    def on_create(self):
        # Put a fresh recipe on the scope;
        self._res.recipe = self._rcs.load_new_recipe()
        # Configure the save reminder;
        self.app.guard_exit('home.recipes.edit', 'RecipeSaveCheckComponent')
        # Go into edit mode;
        self._res.mode = 'edit'
        # Go;
        self.app.goto('home.recipes.edit')

    def on_edit(self):
        self._res.mode = 'edit'
        self.app.goto('home.recipes.search')

    def on_delete(self):
        self.app.goto('home.recipes.search')

    def on_view(self):
        self.app.goto('home.recipes.view')
