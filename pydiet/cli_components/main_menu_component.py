from pyconsoleapp import ConsoleAppComponent

_menu_template = '''
Manage Ingredients      | -ingredients, -i
Manage Recipes          | -recipes, -r
Manage Goals            | -goals, -g
Generate Meal Plans     | -solve, -s
View Meal Plans         | -view, -v
'''


class MainMenuComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self.configure_printer(self.print_menu_view)
        self.configure_responder(self.on_manage_ingredients, args=[
            self.configure_valueless_primary_arg('ingredients', ['-ingredients', '-i'])])
        self.configure_responder(self.on_manage_recipes, args=[
            self.configure_valueless_primary_arg('recipes', ['-recipes', '-r'])])         
        self.configure_responder(self.on_manage_goals, args=[
            self.configure_valueless_primary_arg('goals', ['-goals', '-g'])])                  
        self.configure_responder(self.on_run_optimiser, args=[
            self.configure_valueless_primary_arg('optimiser', ['-optimiser', '-o'])]) 
        self.configure_responder(self.on_view_meal_plans, args=[
            self.configure_valueless_primary_arg('view', ['-view', '-v'])])             

    def print_menu_view(self):
        output = _menu_template
        output = self.app.fetch_component('standard_page_component').print(
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
