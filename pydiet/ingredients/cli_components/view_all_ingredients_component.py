from typing import OrderedDict

from pyconsoleapp import ConsoleAppComponent

from pydiet import repository_service as rps
from pydiet.ingredients import ingredient_edit_service as ies
from pydiet.ingredients import ingredient_service as igs

_TEMPLATE = '''All Ingredients:
----------------
{ingredients_menu}
'''


class ViewAllIngredientsComponent(ConsoleAppComponent):
    def __init__(self, app):
        super().__init__(app)
        self._numbered_ingredients: OrderedDict[int, str] = {}
        self._selected_ingredient_name: str
        self._ies = ies.IngredientEditService()

    def print(self):
        # Form the ingredients list;
        # Load the index of names;
        index = rps.read_ingredient_index()
        # Init the menu string;
        ingredients_menu = ''
        # If there are no ingredients yet;
        if not len(index):
            # Add message to inform user;
            ingredients_menu = 'No ingredients found.'
        else:
            # Build up the ordered dictionary of selection keys and their
            # corresponding ingredients;
            ingredient_names = sorted(list(index.values()))
            for n, ingredient_name in enumerate(ingredient_names, start=1):
                self._numbered_ingredients[n] = ingredient_name
            # Use this dictionary to create the output string;
            for number in self._numbered_ingredients.keys():
                ## Grab the datafile (we need to load to get the status)
                current_ingredient_datafile_name = igs.resolve_ingredient_datafile_name(
                    self._numbered_ingredients[number]
                )
                ## Load the ingredient;
                current_ingredient = igs.load_ingredient(current_ingredient_datafile_name)
                ## Add this to the menu;
                ingredients_menu = ingredients_menu + \
                    '({number}) -- {ingredient_name}: {ingredient_status}\n'.format(
                        number=str(number),
                        ingredient_name=self._numbered_ingredients[number],
                        ingredient_status=igs.summarise_status(current_ingredient)
                    )
        # Place the list into the template;
        output = _TEMPLATE.format(
            ingredients_menu=ingredients_menu
        )
        # Build the template;
        output = self.app.fetch_component('standard_page_component').print(output)
        #
        return output

    def dynamic_response(self, raw_response: str) -> None:
        # Try and parse the response as an integer;
        try:
            response = int(raw_response)
        except ValueError:
            return None
        # If the response matches one of the ingredient numbers;
        try:
            self._selected_ingredient_name = self._numbered_ingredients[response]
        except KeyError:
            return None
        # Load the ingredient into the ies;
        self._ies.datafile_name = igs.resolve_ingredient_datafile_name(
            self._selected_ingredient_name)
        self._ies.ingredient = igs.load_ingredient(
            self._ies.datafile_name)
        # Redirect to the edit page for that ingredient;
        self.app.goto('home.ingredients.edit')
