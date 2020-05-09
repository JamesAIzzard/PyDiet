from typing import TYPE_CHECKING, cast

from pyconsoleapp import ConsoleAppComponent
from pinjector import inject

if TYPE_CHECKING:
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService
    from pydiet.cli.ingredients.ingredient_save_check_component import IngredientSaveCheckComponent
    from pydiet.ingredients import ingredient_service
    from pydiet.data import repository_service

_TEMPLATE = '''Ingredient Search Results:
-------------------------

Select an ingredient:
{results_display}
'''

class IngredientSearchResultsComponent(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self._ies:'IngredientEditService' = inject('pydiet.cli.ingredient_edit_service')
        self._igs:'ingredient_service' = inject('pydiet.ingredient_service')
        self._rp: 'repository_service' = inject('pydiet.repository_service')

    def print(self):
        results_display = ''
        if not len(self._ies.ingredient_search_results):
            results_display = 'No ingredients found.'
        else:
            nmap = self._ies.ingredient_search_result_number_name_map
            for num in nmap.keys():
                results_display = results_display + '({}) -- {}\n'.format(num, nmap[num])
        output = _TEMPLATE.format(results_display=results_display)
        return self.get_component('standard_page_component').print(output)

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
            datafile_name = self._igs.resolve_ingredient_datafile_name(ingredient_name)
            # If the corresponding datafile was found;
            if datafile_name:
                # Populate the datafile name on the ies;
                self._ies.datafile_name = datafile_name
                # If we are on the edit branch;
                if 'home.ingredients.edit' in self.app.route or\
                    'home.ingredients.view' in self.app.route:
                    # Load the ingredient into the ies;
                    self._ies.ingredient = self._igs.load_ingredient(datafile_name)
                    # Configure the save reminder;
                    cast(
                        'IngredientSaveCheckComponent',
                        self.get_component('ingredient_save_check_component')
                    ).guarded_route = 'home.ingredients.edit'
                    self.guard_exit('home.ingredients.edit', 'ingredient_save_check_component')
                    # Redirect to edit;
                    self.goto('home.ingredients.edit')
                # If we are on the delete branch;
                elif 'home.ingredients.delete' in self.app.route:
                    # Load the ingredient into the ies;
                    self._ies.ingredient = self._igs.load_ingredient(datafile_name)     
                    # Move on to confirm deletion;               
                    self.goto('..confirm')
            # If the datafile wasn't found, something is broken;
            else:
                raise ValueError('No datafile was found for {}'.format(ingredient_name))

