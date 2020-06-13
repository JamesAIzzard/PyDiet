from typing import Dict

from pyconsoleapp import parse_tools
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
        self.ingredient_number_map:Dict[int, str] = {}

    def print(self):
        # Catch no-recipe;
        if not self._res.recipe:
            raise AttributeError
        # Build the ingredients list;
        # Tell the user if no ingredients are added yet;
        if len(self._res.recipe.ingredient_amounts) == 0:
            ingredients_list = 'No ingredients added.'
        # Or list any ingredients which have been added;
        else:
            ingredients_list = ''
            for i, ia in enumerate(self._res.recipe.ingredient_amounts.values(), start=1):
                # Build section for ingredients list;
                ingredients_list = ingredients_list + '{ingredient_number}. {ingredient_summary}\n'.format(
                    ingredient_number=i,
                    ingredient_summary=rcs.summarise_ingredient_amount(ia)
                )
                # Add to name-number map;
                self.ingredient_number_map[i] = ia.name
        # Build and return the page output;
        output = _MAIN_TEMPLATE.format(ingredients_list=ingredients_list)
        output = self.app.fetch_component(
            'standard_page_component').print(output)
        return output

    def on_save(self):
        self._res.save_changes()

    def on_add_ingredient(self):
        self.app.goto('home.recipes.edit.ingredients.search')

    def dynamic_response(self, raw_response: str) -> None:
        # Try and parse the raw response into a letter and integer;
        try:
            letter, ing_number = parse_tools.parse_letter_and_integer(
                raw_response)
        # Ignore input if it doesn't parse;
        except parse_tools.LetterIntegerParseError:
            return
        # Check the integer references an ingredient on the list;
        if ing_number > len(self._res.recipe.ingredient_amounts) or ing_number < 1:
            return
        # If we are removing an ingredient;
        if letter == 'r':
            del self._res.recipe.ingredient_amounts[self.ingredient_number_map[ing_number]]
        # If we are editing the nominal amount of an ingredient;
        elif letter == 'e':
            # Load the ingredient amount onto the res;
            self._res.ingredient_amount = self._res.recipe.ingredient_amounts[self.ingredient_number_map[ing_number]]
            # Redirect to qty edit page;
            self.app.goto('home.recipes.edit.ingredients.set_ingredient_qty')
        # If we are editing the allowable variation for an ingredient;
        elif letter == 'v':
            # Load the ingredient amount onto the res;
            self._res.ingredient_amount = self._res.recipe.ingredient_amounts[self.ingredient_number_map[ing_number]]
            # Redirect to qty edit page;
            self.app.goto('home.recipes.edit.ingredients.set_ingredient_variations')

