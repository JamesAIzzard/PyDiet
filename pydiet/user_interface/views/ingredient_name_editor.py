from pydiet.user_interface.views.view import View
from pydiet.services import services

TEXT = '''Enter ingredient name:'''

class IngredientNameEditor(View):
    def __init__(self):
        self.text = TEXT

    def response_action(self, res):
        if not res == '':    
            services.ingredient.current_data['name'] = res
        return "ingredient_editor"

