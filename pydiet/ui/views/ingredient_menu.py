from pydiet.ui.views.view import View
import pydiet.data.repository_service as repo

TEXT = '''Choose one of the following options:
n -> Create new ingredient datafile.
---------------------------
'''


class IngredientMenu(View):
    def __init__(self):
        self.text = TEXT

    def action(self, choice):
        if choice == 'n':
            print('Creating new ingredient...')
            # repo.create_new_ingredient_datafile()
            return 'main_menu'
