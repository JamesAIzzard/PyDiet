import os
from pydiet.ui.exceptions import UnknownViewError
from pydiet.ui.views.main_menu import MainMenu
from pydiet.ui.views.ingredient_menu import IngredientMenu

HEADER_TEXT = '''
PyDiet:
-----------------------------------
b -> go back
q -> quit
-----------------------------------
'''


class UI():
    def __init__(self):
        self.views = {}
        self.view_name_stack = []
        self.header = HEADER_TEXT

    def go_to(self, view_name):
        if len(self.view_name_stack) == 0:
            self.view_name_stack.append(view_name)
        elif not self.view_name_stack[-1] == view_name:
            self.view_name_stack.append(view_name)
        print(HEADER_TEXT)
        choice = input(self.views[view_name].text)
        if choice == 'b':
            if len(self.view_name_stack) > 1:
                self.clear()
                self.view_name_stack.pop()
                back_screen_name = self.view_name_stack.pop()
                self.go_to(back_screen_name)
        elif choice == 'q':
            return
        else:
            try:
                view_name = self.views[view_name].action(choice)
                self.clear()
                self.go_to(view_name)
            except UnknownViewError as ex:
                print(ex.message, ex.choice)
                self.go_to(view_name)

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')


ui = UI()
ui.views['main_menu'] = MainMenu()
ui.views['ingredient_menu'] = IngredientMenu()
