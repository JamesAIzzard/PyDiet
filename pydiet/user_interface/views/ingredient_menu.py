from pydiet.user_interface.views.view import View
from pydiet.services import services

TEXT = '''Choose one of the following options:
c -> Create a new ingredient.
r -> Rename an ingredient.
u -> Update an ingredient.
d -> Delete an ingredient.
'''


class IngredientMenu(View):
	def __init__(self):
		self.text = TEXT

	def startup_action(self):
		services.ui.display_data(services.ingredient.current_data)

	def response_action(self, res):
		if res == 'c':
			services.ingredient.current_data = \
				services.ingredient.get_data_template()
			return "ingredient_editor"
