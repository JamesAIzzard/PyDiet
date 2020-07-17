from pyconsoleapp import ConsoleAppComponent

_MENU_TEMPLATE = '''
-ingredients, -i    -> Manage ingredients.
-recipes, -r        -> Manage recipes.
-goals, -g          -> Manage goals.
-solve, -s          -> Generate meal plans.
-view, -v           -> View meal plans.
'''


class MainMenuComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self.set_print_function(self.print_menu)
        self.set_response_function(['-ingredients', '-i'], self.on_manage_ingredients)
        self.set_response_function(['-recipes', '-r'], self.on_manage_recipes)
        self.set_response_function(['-goals', '-g'], self.on_manage_goals)
        self.set_response_function(['-solve', '-s'], self.on_run_optimiser)
        self.set_response_function(['-view', '-v'], self.on_view_meal_plans)

    def print_menu(self):
        output = _MENU_TEMPLATE
        output = self.app.fetch_component('standard_page_component').call_print(
            page_content=output, 
            page_title='Main Menu')
        return output

    def on_manage_ingredients(self):
        self.app.goto('home.ingredients')

    def on_manage_recipes(self):
        self.app.goto('home.recipes')

    def on_manage_goals(self):
        self.app.goto('home.goals')

    def on_run_optimiser(self):
        pass

    def on_view_meal_plans(self):
        pass
