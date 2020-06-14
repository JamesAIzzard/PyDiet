from typing import OrderedDict

from pyconsoleapp import ConsoleAppComponent

from pydiet import repository_service as rps
from pydiet.recipes import recipe_edit_service as res
from pydiet.recipes import recipe_service as rcs

_TEMPLATE = '''All Recipes:
---------------
{recipes_menu}
'''


class ViewAllRecipesComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self._res = res.RecipeEditService()
        self._numbered_recipes: OrderedDict[int, str] = {}
        self._selected_recipe_name: str

    def print(self, *args, **kwargs) -> str:
        # Load the index of recipe names;
        index = rps.read_recipe_index()
        # Build the menu;
        recipes_menu = ''
        # If no recipes yet;
        if not len(index):
            recipes_menu = 'No recipes found.'
        # Otherwise, build a numbered dict of recipes;
        # Dict is ordered to maintain numerical order;
        else:
            recipe_names = sorted(list(index.values()))
            for n, recipe_name in enumerate(recipe_names, start=1):
                self._numbered_recipes[n] = recipe_name
            # Create the output string;
            for number in self._numbered_recipes.keys():
                recipes_menu = recipes_menu + '({number}) -- {recipe_name}\n'.format(
                    number=str(number),
                    recipe_name=self._numbered_recipes[number]
                )
        # Place the list into the template;
        output = _TEMPLATE.format(recipes_menu=recipes_menu)
        # Build & return the final page;
        output = self.app.fetch_component(
            'standard_page_component').print(output)
        return output

    def dynamic_response(self, raw_response: str) -> None:
        # Try and parse the response as an integer;
        try:
            response = int(raw_response)
        except ValueError:
            return
        # If the response matches one of the recipe numbers;
        try:
            self._selected_recipe_name = self._numbered_recipes[response]
        except KeyError:
            return
        # Load the recipe into the res;
        self._res.datafile_name = rcs.convert_recipe_name_to_datafile_name(
            self._selected_recipe_name)
        self._res.recipe = rcs.load_recipe(self._res.datafile_name)
        # Redirect to the edit page for that recipe;
        self.app.goto('home.recipes.edit')
