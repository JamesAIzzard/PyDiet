from pyconsoleapp.console_app_component import ConsoleAppComponent

_MENU_TEMPLATE = '''Choose an option:
(1) - Manage ingredients.
(2) - Manage recipes.
(3) - Manage user goals.
(4) - Run optimiser.
'''


class MainMenu(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self.set_option_response('1', self.on_manage_ingredients)
        self.set_option_response('2', self.on_manage_recipes)
        self.set_option_response('3', self.on_manage_goals)
        self.set_option_response('4', self.on_run_optimiser)

    def run(self):
        output = _MENU_TEMPLATE
        output = self.run_parent('StandardPage', output)
        return output

    def on_manage_ingredients(self):
        self.app.navigate(['home', 'ingredients'])

    def on_manage_recipes(self):
        raise NotImplementedError

    def on_manage_goals(self):
        raise NotImplementedError

    def on_run_optimiser(self):
        raise NotImplementedError