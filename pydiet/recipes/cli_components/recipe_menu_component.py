from pyconsoleapp import ConsoleAppComponent

from pydiet.recipes import recipe_service as rcs
from pydiet.recipes import recipe_edit_service as res

_MENU_TEMPLATE = '''Choose an option:
(1) -- Create a new recipe.
(2) -- Edit an existing recipe.
(3) -- Delete an existing recipe.
(4) -- View recipes.
'''


class RecipeMenuComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self._res = res.RecipeEditService()
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
        self._res.recipe = rcs.load_new_recipe()
        # Configure the save reminder;
        self.app.guard_exit('home.recipes.edit', 'RecipeSaveCheckComponent')
        # Go;
        self.app.goto('home.recipes.edit')

    def on_edit(self):
        self.app.goto('home.recipes.search')

    def on_delete(self):
        # Move onto the delete search;
        self.app.goto('home.recipes.delete.search')

    def on_view(self):
        # Ask if the user wants to view a particular recipe;
        self.app.goto('home.recipes.ask_search')
