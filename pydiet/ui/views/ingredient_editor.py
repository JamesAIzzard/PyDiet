from pydiet.ui.views.view import View

TEXT = '''Ingredient Editor
----------------------------
Choose an option:
m -> mandatory fields

1 -> name
2 -> cost
3 -> flags
4 -> macronutrient totals
5 -> micronutrient totals
'''

class IngredientEditor(View):
    def __init__(self):
        self.text = TEXT

    def action(self, choice):
        if choice == 'm':
            return 'ingredient_mandatory_fields_editor'
        elif choice == '1':
            return 'ingredient_name_editor'

