from pydiet.user_interface.views.view import View
from pydiet.services import services as services

TEXT = '''Choose an option to edit:
m -> mandatory fields
1 -> name
2 -> cost
3 -> flags
4 -> macronutrient totals
5 -> micronutrient totals
----------------------------
'''

class IngredientEditor(View):
    def __init__(self):
        self.text = TEXT

    def _startup_action(self):
        services.ui.display_data(services.ingredient.current_data)

    def response_action(self, res):
        if res == 'm':
            return 'ingredient_mandatory_fields_editor'
        elif res == '1':
            return 'ingredient_name_editor'

