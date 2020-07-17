from pyconsoleapp import ConsoleAppComponent

from pydiet.ingredients import ingredient_edit_service as ies
from pydiet.ingredients import ingredient_service as igs

_MENU_TEMPLATE = '''Choose an option:
(1) -- Create a new ingredient.
(2) -- Edit an existing ingredient.
(3) -- Delete an existing ingredient.
(4) -- View ingredients.
'''


class IngredientMenuComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
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
        output = self.app.fetch_component('standard_page_component').call_print(output)
        return output

    def on_create(self):
        # Put a fresh ingredient on the scope;
        self._ies.ingredient = igs.load_new_ingredient()
        # Configure the save reminder;
        self.app.guard_exit('home.ingredients.edit', 'IngredientSaveCheckComponent')
        # Go;
        self.app.goto('home.ingredients.edit')

    def on_edit(self):
        # Go to the ingredient search page;
        self.app.goto('home.ingredients.search')

    def on_delete(self):
        # Go to search;
        self.app.goto('home.ingredients.delete.search')

    def on_view(self):
        # Go to view menu;
        self.app.goto('home.ingredients.ask_search')
