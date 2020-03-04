from pyconsoleapp.console_app_component import ConsoleAppComponent

_TEMPLATE = '''Choose an option:
(1) - Set ingredient name.
(2) - Set ingredient flags.
(3) - Set a macronutrient.
(4) - Set a micronutrient.
'''

GUARD_ROUTE = ['home', 'ingredients', 'new']


class IngredientEditMenu(ConsoleAppComponent):
    def __init__(self):
        super().__init__()

    def run(self):
        output = _TEMPLATE
        output = self.run_parent('standard_page', output)
        return output

    def on_set_name(self):
        self.app.guard_exit(GUARD_ROUTE, 'ingredient_save_check')
        self.app.navigate(['.', 'name'])


ingredient_edit_menu = IngredientEditMenu()
ingredient_edit_menu.set_option_response('1', 'on_set_name')
