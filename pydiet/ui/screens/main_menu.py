from pydiet.ui.screens.screen import Screen
from pydiet.ui.screens.ingredient_menu import IngredientMenu
from pydiet.ui.screens.recipe_menu import RecipeMenu

TEXT = '''
PYDIET - Main Menu
-------------
Choose one of the following options:
i -> edit/create/delete ingredients
r -> edit/create/delete recipes
g -> start optimisation run
-----------------------------

'''

class MainMenu(Screen):
    def __init__(self):
        self.text = TEXT

    def run(self):
        option = input(self.text)
        if option == "i":
            self.go_to(IngredientMenu)
        elif option == "r":
            self.go_to(RecipeMenu)
        elif option == "g":
            _ = input("Starting Optimisation Run...")