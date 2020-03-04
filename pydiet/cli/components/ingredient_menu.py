from pyconsoleapp.console_app_component import ConsoleAppComponent

_MENU_TEMPLATE = '''Choose an option:
(1) - Create a new ingredient.
(2) - Edit an existing ingredient.
(3) - Delete an existing ingredient.
(4) - View an existing ingredient.
'''


class IngredientMenuComponent(ConsoleAppComponent):

    def run(self):
        self.app.guard_entrance(['.', 'new'], 'ingredient_create_check')
        output = _MENU_TEMPLATE
        output = self.run_parent('standard_page', output)
        return output

    def on_create(self):
        # self.app.set_window_text('Some test text.')
        # self.app.show_text_window()
        self.app.navigate(['.', 'new'])

    def on_edit(self):
        raise NotImplementedError

    def on_delete(self):
        raise NotImplementedError

    def on_view(self):
        raise NotImplementedError
    
    def dynamic_response(self, response):
        pass
        # self.app.set_window_text(response)
        # self.app.show_text_window()
    
ingredient_menu = IngredientMenuComponent()
ingredient_menu.set_option_response('1', 'on_create')
ingredient_menu.set_option_response('2', 'on_edit')
ingredient_menu.set_option_response('3', 'on_delete')
ingredient_menu.set_option_response('4', 'on_view')
