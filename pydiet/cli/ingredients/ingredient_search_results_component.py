from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent
from pinjector import inject

if TYPE_CHECKING:
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService
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
            # Resolve the datafile name for the ingredient;
            self._ies.datafile_name = self._rp.resolve_ingredient_datafile_name(
                self._ies.ingredient_search_result_number_name_map[response])
            # Load the ingredient into the ies;
            self._ies.ingredient = self._rp.read_ingredient(self._ies.datafile_name)
            # Configure the save reminder;
            self.get_component('ingredient_save_check_component').guarded_route = \
                'home.ingredients.edit'
            self.guard_exit('home.ingredients.edit', 'ingredient_save_check_component')
            # Redirect to edit;
            self.goto('home.ingredients.edit')

