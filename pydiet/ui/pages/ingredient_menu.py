from pyconsoleapp.console_app_page import ConsoleAppPage
from pyconsoleapp.components.header import header
from pydiet.ui.components.ingredient_menu import ingredient_menu as ingredient_menu_component

class IngredientMenu(ConsoleAppPage):
    pass

ingredient_menu = IngredientMenu()
ingredient_menu.add_component(header)
ingredient_menu.add_component(ingredient_menu_component)