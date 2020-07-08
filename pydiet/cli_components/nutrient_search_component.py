from typing import List, Dict
from heapq import nlargest

from pyconsoleapp import ConsoleAppComponent, search_tools, menu_tools

from pydiet.ingredients import ingredient_service

_SEARCH_TEMPLATE = '''
Enter nutrient name:
'''

_RESULTS_TEMPLATE = '''
Select a nutrient:
{search_results}
'''

class NutrientSearchComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self.configure_states(['SEARCH', 'RESULTS'])
        self.state = 'SEARCH'
        self.set_print_function(self.print_search, states=['SEARCH'])
        self.set_print_function(self.print_results, states=['RESULTS'])     
        self.set_any_response_function(self.on_search, states=['SEARCH'])
        self.set_any_response_function(self.on_result_selection, states=['RESULTS'])   
        self.chosen_nutrient_name:List[str]
        self.return_route:str
        self.search_result_number_map:Dict[int, str] = {}

    def on_run(self) -> None:
        if not self.chosen_nutrient_name or not self.return_route:
            raise AttributeError

    def print_search(self)->str:
        output = _SEARCH_TEMPLATE
        return self.app.fetch_component('standard_page_component').print(output)

    @property
    def search_results_text(self)->str:
        output = ''
        for result_num in self.search_result_number_map.keys():
            output = output + '{result_num} -> {result_name}\n'.format(
                result_num=result_num,
                result_name=self.search_result_number_map[result_num]
            )
        return output

    def print_results(self)->str:
        output = _RESULTS_TEMPLATE.format(search_results=self.search_results_text)
        return self.app.fetch_component('standard_page_component').print(output)

    def on_search(self, response) -> None:
        # Load a list of all nutrient names;
        nutrient_names = ingredient_service.get_all_nutrient_names()
        # Score each item against the names of the search term;
        results = search_tools.score_similarity(nutrient_names, response)
        # Map the 5 largest scores to numbers;
        self.search_result_number_map = menu_tools.create_number_name_map(
            nlargest(5, results, key=results.get))
        # Change state to show results;
        self.state = 'RESULTS'
        # Finalse response;
        self.app.stop_responding()

    def on_result_selection(self, response:str) -> None:
        # Check the response refers to a result on the page;
        try:
            selection = int(response)
        except ValueError:
            self.app.info_message = 'Select a nutrient by entering its number.'
            return
        # Place the selected nutrient name on the object;
        self.chosen_nutrient_name[0] = self.search_result_number_map[selection]
        # Stop response processing;
        self.app.stop_responding()