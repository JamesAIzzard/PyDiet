from pyconsoleapp.console_app_component import ConsoleAppComponent

_MENU_TEMPLATE = '''Choose an option:
(1) - Manage ingredients.
(2) - Manage recipes.
(3) - Manage user goals.
(4) - Run optimiser.
'''


class MainMenuComponent(ConsoleAppComponent):

    def run(self):
        output = _MENU_TEMPLATE
        output = self.run_parent('standard_page', output)
        return output

    def on_manage_ingredients(self):
        self.app.info_message = 'Navigation success :)'
        self.app.navigate(['home', 'ingredients'])

    def on_manage_recipes(self):
        raise NotImplementedError

    def on_manage_goals(self):
        raise NotImplementedError

    def on_run_optimiser(self):
        raise NotImplementedError


main_menu = MainMenuComponent()
main_menu.set_option_response('1', 'on_manage_ingredients')
main_menu.set_option_response('2', 'on_manage_recipes')
main_menu.set_option_response('3', 'on_manage_goals')
main_menu.set_option_response('4', 'on_run_optimiser')
