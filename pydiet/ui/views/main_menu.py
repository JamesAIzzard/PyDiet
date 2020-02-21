from pydiet.ui.views.view import View

TEXT = '''Choose one of the following options:
i -> edit/create/delete ingredients
r -> edit/create/delete recipes
g -> start optimisation run
-----------------------------

'''

class MainMenu(View):
    def __init__(self):
        self.text = TEXT
    def action(self, choice):
        if choice == 'i':
            return 'ingredient_menu'
        elif choice == 'r':
            raise NotImplementedError
        elif choice == 'g':
            raise NotImplementedError