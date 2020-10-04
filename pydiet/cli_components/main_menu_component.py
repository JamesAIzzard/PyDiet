from pyconsoleapp import ConsoleAppComponent

_menu_template = '''
Manage Ingredients      | -ingr
Manage Recipes          | -recp
Manage Goals            | -goal
Generate Meal Plans     | -solv
View Meal Plans         | -view
'''


class MainMenuComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self.configure_printer(self.print_menu_view)
        self.configure_responder(self.on_manage_ingredients, args=[
            self.configure_valueless_primary_arg('ingredients', ['-ingr'])])
        self.configure_responder(self.on_manage_recipes, args=[
            self.configure_valueless_primary_arg('recipes', ['-recp'])])         
        self.configure_responder(self.on_manage_goals, args=[
            self.configure_valueless_primary_arg('goals', ['-goal'])])                  
        self.configure_responder(self.on_run_optimiser, args=[
            self.configure_valueless_primary_arg('solve', ['-solv'])]) 
        self.configure_responder(self.on_view_meal_plans, args=[
            self.configure_valueless_primary_arg('view', ['-view'])])             

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
        pass

    def on_run_optimiser(self):
        pass

    def on_view_meal_plans(self):
        pass
