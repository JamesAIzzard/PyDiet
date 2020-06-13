from pyconsoleapp import ConsoleAppComponent

from pydiet.ingredients import ingredient_edit_service as ies
from pydiet.ingredients import ingredient_service as igs
from pydiet.recipes import recipe_service as rcs
from pydiet.recipes import recipe_edit_service as res

_TEMPLATE = '''Ingredient Search Results:
-------------------------

Select an ingredient:
{results_display}
'''


class IngredientSearchResultsComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self._ies = ies.IngredientEditService()
        self._res = res.RecipeEditService()

    def print(self):
        results_display = ''
        if not len(self._ies.ingredient_search_results):
            results_display = 'No ingredients found.'
        else:
            nmap = self._ies.ingredient_search_result_number_name_map
            for num in nmap.keys():
                results_display = results_display + \
                    '({}) -- {}\n'.format(num, nmap[num])
        output = _TEMPLATE.format(results_display=results_display)
        return self.app.fetch_component('standard_page_component').print(output)

    def dynamic_response(self, response):
        # Try and parse the response as an integer;
        try:
            response = int(response)
        except ValueError:
            return None
        # If the option matches one on-screen;
        if response in self._ies.ingredient_search_result_number_name_map.keys():
            # Convert the response into an ingredient name;
            ingredient_name = self._ies.ingredient_search_result_number_name_map[response]
            # Resolve the datafile name for the ingredient;
            datafile_name = igs.convert_ingredient_name_to_datafile_name(
                ingredient_name)
            # If the corresponding datafile was found;
            if datafile_name:
                # Populate the datafile name on the ies;
                self._ies.datafile_name = datafile_name
                # If we are editing an ingredient;
                if 'home.ingredients.search_results' in self.app.route:
                    # Load the ingredient into the ies;
                    self._ies.ingredient = igs.load_ingredient(
                        datafile_name)
                    # Configure the save reminder;
                    self.app.guard_exit('home.ingredients.edit',
                                        'IngredientSaveCheckComponent')
                    # Redirect to edit;
                    self.app.goto('home.ingredients.edit')
                # If we are deleting an ingredient;
                elif 'home.ingredients.delete' in self.app.route:
                    # Load the ingredient into the ies;
                    self._ies.ingredient = igs.load_ingredient(
                        datafile_name)
                    # Move on to confirm deletion;
                    self.app.goto('home.ingredients.delete.confirm')
                # If we are selecting an ingredient to add to a recipe;
                elif 'home.recipes.edit.ingredients.search_results' in self.app.route:
                    # Load the ingredient;
                    i = igs.load_ingredient(datafile_name)
                    # Add the ingredient amount to the current recipe;
                    self._res.recipe.add_ingredient(i)
                    # Store the ingredient amount on the recipe edit service;
                    self._res.ingredient_amount = self._res.recipe.ingredient_amounts[ingredient_name]
                    # Head back to the edit recipe ingredients page;
                    self.app.goto('home.recipes.edit.ingredients')
