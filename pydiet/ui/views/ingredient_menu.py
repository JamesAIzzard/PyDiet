from pydiet.ui.views.view import View
import pydiet.data.repository_service as repo
import pydiet.ingredients.ingredient_service as iservice
from pydiet.ingredients.ingredient import Ingredient

TEXT = '''Ingredient Menu
---------------------------
Choose one of the following options:
c -> Create a new ingredient.
r -> Rename an ingredient.
u -> Update an ingredient.
d -> Delete an ingredient.
'''


class IngredientMenu(View):
	def __init__(self):
		self.text = TEXT

	def action(self, choice):
		if choice == 'c':
			iservice.current_ingredient_data = \
				iservice.get_ingredient_data_template()
			return "ingredient_editor"
