from pyconsoleapp import ConsoleAppComponent

from pydiet.recipes import recipe_edit_service as res

_TEMPLATE = '''How much {ingredient_name} is there in the {recipe_name} recipe?
(e.g 100g, 20L 0.5kg etc.)

'''

class EditIngredientQtyComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self._res = res.RecipeEditService()

    def print(self):
        output = _TEMPLATE.format(
            ingredient_name=self._res.ingredient.name,
            recipe_name=self._res.recipe.name
        )
        output = self.app.fetch_component('standard_page_component').print(output)
        return output

    def dynamic_response(self, raw_response: str) -> None:
        raise NotImplementedError