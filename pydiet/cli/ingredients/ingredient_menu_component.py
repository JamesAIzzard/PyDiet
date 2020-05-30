from pyconsoleapp import ConsoleAppComponent

from pydiet.cli.ingredients import ingredient_edit_service as ies
from pydiet.ingredients import ingredient_service as igs

_MENU_TEMPLATE = '''Choose an option:
(1) -- Create a new ingredient.
(2) -- Edit an existing ingredient.
(3) -- Delete an existing ingredient.
(4) -- View ingredients.
'''


class IngredientMenuComponent(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self._ies = ies.IngredientEditService()
        self.set_option_response('1', self.on_create)
        self.set_option_response('2', self.on_edit)
        self.set_option_response('3', self.on_delete)
        self.set_option_response('4', self.on_view)

    def run(self):
        self._ies.ingredient = None
        self._ies.datafile_name = None

    def print(self):
        output = _MENU_TEMPLATE
        output = self.app.fetch_component('standard_page_component').print(output)
        return output

    def on_create(self):
        # Put a fresh ingredient on the scope;
        self._ies.ingredient = igs.load_new_ingredient()
        # Configure the save reminder;
        self.app.guard_exit('home.ingredients.edit', 'IngredientSaveCheckComponent')
        # Go into edit mode;
        self._ies.mode = 'edit'
        # Go;
        self.app.goto('home.ingredients.edit')

    def on_edit(self):
        # Go into edit mode;
        self._ies.mode = 'edit'
        # Go to the ingredient search page;
        self.app.goto('home.ingredients.search')

    def on_delete(self):
        # Go into delete mode;
        self._ies.mode = 'delete'
        # Go to search;
        self.app.goto('home.ingredients.search')

    def on_view(self):
        # Ultimately view will lead to editing an ingredient;
        self._ies.mode = 'edit'
        # Go to view menu;
        self.app.goto('home.ingredients.ask_search')
