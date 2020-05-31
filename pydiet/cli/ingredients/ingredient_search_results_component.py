from pyconsoleapp import ConsoleAppComponent

from pydiet.cli.ingredients import ingredient_edit_service as ies
from pydiet.ingredients import ingredient_service as igs

_TEMPLATE = '''Ingredient Search Results:
-------------------------

Select an ingredient:
{results_display}
'''


class IngredientSearchResultsComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self._ies = ies.IngredientEditService()

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
            datafile_name = igs.resolve_ingredient_datafile_name(
                ingredient_name)
            # If the corresponding datafile was found;
            if datafile_name:
                # Populate the datafile name on the ies;
                self._ies.datafile_name = datafile_name
                # If we are editing;
                if self._ies.mode == 'edit':
                    # Load the ingredient into the ies;
                    self._ies.ingredient = igs.load_ingredient(
                        datafile_name)
                    # Configure the save reminder;
                    self.app.guard_exit('home.ingredients.edit',
                                        'IngredientSaveCheckComponent')
                    # Redirect to edit;
                    self.app.goto('home.ingredients.edit')
                # If we are deleting;
                elif self._ies.mode == 'delete':
                    # Load the ingredient into the ies;
                    self._ies.ingredient = igs.load_ingredient(
                        datafile_name)
                    # Move on to confirm deletion;
                    self.app.goto('home.ingredients.delete.confirm')
            # If the datafile wasn't found, something is broken;
            else:
                raise ValueError(
                    'No datafile was found for {}'.format(ingredient_name))
