from pyconsoleapp.console_app_component import ConsoleAppComponent
from pydiet.injector import injector
from pydiet.ingredients.ingredient import Ingredient

_MENU_TEMPLATE = '''Choose an option:
1 -> Create a new ingredient.
2 -> Edit an existing ingredient.
3 -> Delete an existing ingredient.
4 -> View an existing ingredient.
'''


class IngredientMenuComponent(ConsoleAppComponent):

    def get_screen(self):
        return _MENU_TEMPLATE

    def on_create(self):
        i_data = injector.ingredient_service.get_data_template()
        i = Ingredient(i_data)
        injector.ingredient_service.current_ingredient = i
        self.app.set_window_text(i.summary)
        self.app.show_text_window()
        self.app.navigate(['home', 'ingredients', 'new'])

    def on_edit(self):
        self.app.navigate(['home', 'ingredients', 'edit'])

    def on_delete(self):
        raise NotImplementedError

    def on_view(self):
        raise NotImplementedError
    
ingredient_menu = IngredientMenuComponent()
ingredient_menu.set_option_response('1', 'on_create')
ingredient_menu.set_option_response('2', 'on_edit')
ingredient_menu.set_option_response('3', 'on_delete')
ingredient_menu.set_option_response('4', 'on_view')