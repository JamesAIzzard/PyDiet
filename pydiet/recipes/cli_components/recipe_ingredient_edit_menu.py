from pydiet.ingredients import ingredient_amount
from pyconsoleapp import ConsoleAppComponent

from pydiet.recipes import recipe_edit_service as res
from pydiet.recipes import recipe_service as rcs

_MAIN_TEMPLATE = '''Recipe Ingredient Editor:
-------------------------

Ingredient List:
{ingredients_list}

(s)  -- Save recipe.
(a)  -- Add an ingredient.
(r*) -- Remove an ingredient.
(e*) -- Edit the amount of an ingredient.
(v*) -- Edit an ingredient's variation allowances.
'''

class RecipeIngredientEditMenu(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self._res = res.RecipeEditService()
        self.set_option_response('a', self.on_add_ingredient)
        self.set_option_response('s', self.on_save)

    def print(self):
        # Catch no-recipe;
        if not self._res.recipe:
            raise AttributeError
        # Build the ingredients list;
        ## Tell the user if no ingredients are added yet;
        if len(self._res.recipe.ingredient_amounts) == 0:
            ingredients_list = 'No ingredients added.'
        ## Or list any ingredients which have been added;
        else:
            ingredients_list = ''
            for i, ia in enumerate(self._res.recipe.ingredient_amounts.values(), start=1):
                ingredients_list = ingredients_list + '{ingredient_number}. {ingredient_summary}\n'.format(
                    ingredient_number=i,
                    ingredient_summary=rcs.summarise_ingredient_amount(ia)
                )
        # Build and return the page output;
        output = _MAIN_TEMPLATE.format(ingredients_list=ingredients_list)
        output = self.app.fetch_component('standard_page_component').print(output)
        return output

    def on_save(self):
        self._res.save_changes()

    def on_add_ingredient(self):
        self.app.goto('home.recipes.edit.ingredients.search')

    def dynamic_response(self, raw_response: str) -> None:
        raise NotImplementedError