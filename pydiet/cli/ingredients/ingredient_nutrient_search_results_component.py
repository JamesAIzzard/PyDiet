from pyconsoleapp import ConsoleAppComponent

from pydiet.cli.ingredients import ingredient_edit_service as ies
from pydiet.ingredients import ingredient_service as igs

_TEMPLATE = '''Nutrient Search Results:
------------------------

Select a nutrient:
{results_display}
'''


class IngredientNutrientSearchResultsComponent(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self._ies = ies.IngredientEditService()

    def print(self):
        results_display = ''
        nmap = self._ies.nutrient_search_result_number_name_map
        for num in nmap.keys():
            na = self._ies.ingredient.get_nutrient_amount(nmap[num])
            summary = igs.summarise_nutrient_amount(na)
            results_display = \
                results_display + '({}) -- {}\n'.format(
                    num,
                    summary
                )
        output = _TEMPLATE.format(
            results_display=results_display
        )
        return self.app.fetch_component('standard_page_component').print(output)

    def dynamic_response(self, response):
        # Try and parse the response as a integer;
        try:
            response = int(response)
        except ValueError:
            return None
        # If the option matches one on-screen;
        if response in self._ies.nutrient_search_result_number_name_map.keys():
            # Set the current nutrient amount and navigate to edit;
            nutrient_name = \
                self._ies.nutrient_search_result_number_name_map[response]
            self._ies.current_nutrient_amount = \
                self._ies.ingredient.get_nutrient_amount(nutrient_name)
            self.app.goto(
                'home.ingredients.edit.nutrients.nutrient_ingredient_qty')
