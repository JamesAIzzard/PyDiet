import os
from pydiet.ui.exceptions import UnknownViewError
from pydiet.ui.views.main_menu import MainMenu
from pydiet.ui.views.ingredient_menu import IngredientMenu
from pydiet.ui.views.ingredient_editor import IngredientEditor

HEADER_TEXT = '''
PyDiet:
=======
b -> go back
q -> quit
-----------------------------------'''


class UI():
    def __init__(self):
        self.views = {}
        self.view_name_stack = []
        self.header = HEADER_TEXT

    def run(self):
        screen_name = "main_menu"
        self.view_name_stack.append(screen_name)
        option = None
        while not option == 'q':
            if not screen_name in self.views.keys():
                screen_name = self.view_name_stack[-1]
            else:
                if not screen_name == self.view_name_stack[-1]:
                    self.view_name_stack.append(screen_name)
                self.clear()
                print(HEADER_TEXT)
                option = input(self.views[screen_name].text)
                if option == "b":
                    if len(self.view_name_stack) > 1:
                        self.view_name_stack.pop()
                        screen_name = self.view_name_stack[-1]
                else:
                    screen_name = self.views[screen_name].action(option)

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')


ui = UI()
ui.views['main_menu'] = MainMenu()
ui.views['ingredient_menu'] = IngredientMenu()
ui.views['ingredient_editor'] = IngredientEditor()
