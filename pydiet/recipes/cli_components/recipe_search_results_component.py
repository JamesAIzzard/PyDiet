from pyconsoleapp import ConsoleAppComponent

from pydiet.recipes import recipe_edit_service as res
from pydiet.recipes import recipe_service as rcs

_TEMPLATE = '''Recipe Search Results:
----------------------

Select an recipe:
{results_display}
'''


class RecipeSearchResultsComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self._res = res.RecipeEditService()

    def print(self):
        results_display = ''
        if not len(self._res.recipe_name_search_results):
            results_display = 'No recipes found.'
        else:
            nmap = self._res.recipe_search_result_number_name_map
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
        if response in self._res.recipe_search_result_number_name_map.keys():
            # Convert the response into an recipe name;
            recipe_name = self._res.recipe_search_result_number_name_map[response]
            # Resolve the datafile name for the recipe;
            self._res.datafile_name = rcs.resolve_recipe_datafile_name(
                recipe_name)
            # If we are in edit mode;
            if self._res.mode == 'edit':
                # Load the ingredient into the res;
                self._res.recipe = rcs.load_recipe(
                    self._res.datafile_name)
                # Configure the save reminder;
                self.app.guard_exit('home.recipes.edit',
                                    'RecipeSaveCheckComponent')
                # Redirect to edit;
                self.app.goto('home.recipes.edit')
            # If we are in delete mode;
            elif self._res.mode == 'delete':
                # Load the ingredient into the res;
                self._res.recipe = rcs.load_recipe(
                    self._res.datafile_name)
                # Move on to confirm deletion;
                self.app.goto('home.recipes.confirm_delete')
