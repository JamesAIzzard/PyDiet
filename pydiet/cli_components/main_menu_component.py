from pyconsoleapp import ConsoleAppComponent

_MENU_TEMPLATE = '''Choose an option:
(1) -- Manage ingredients.
(2) -- Manage recipes.
(3) -- Manage objectives.
(4) -- Generate meal plans.
(5) -- View meal plans.
'''


class MainMenuComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self.set_option_response('1', self.on_manage_ingredients)
        self.set_option_response('2', self.on_manage_recipes)
        self.set_option_response('3', self.on_manage_goals)
        self.set_option_response('4', self.on_run_optimiser)

    def print(self):
        output = _MENU_TEMPLATE
        output = self.app.fetch_component('standard_page_component').print(output)
        return output

    def on_manage_ingredients(self):
        # Navigate;
        self.app.goto('.ingredients')

    def on_manage_recipes(self):
        self.app.goto('.recipes')

    def on_manage_goals(self):
        pass

    def on_run_optimiser(self):
        pass
