from typing import Callable, List

from pyconsoleapp import ConsoleAppComponent

from pydiet.ingredients import ingredient_service as igs
from pydiet.ingredients import ingredient_edit_service as ies

_search_template = '''
Enter ingredient name and press enter | [ingredient name]

'''

_results_template = '''
Choose a result number | [number]
{results}

--------------------------------------
Search Again    | -retry, -r
'''


class IngredientSearchComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self._show_num_results:int = 5
        self.on_ingredient_found:Callable
        self._results:List[str] = []

        self.configure_states(['search', 'results'])

        # Configure search state;
        self.configure_printer(self.print_search_view, states=['search'])
        self.configure_responder(self.on_search_entered, states=['search'], args=[
            self.configure_markerless_primary_arg('search_term')
        ])

        # Configure results state;
        self.configure_printer(self.print_results_view, states=['results'])
        self.configure_responder(self.on_result_selected, states=['results'], args=[
            self.configure_markerless_primary_arg('result_num', validators=[
                self.validate_result_num])
        ])
        self.configure_responder(self.on_retry_search, states=['results'], args=[
            self.configure_valueless_primary_arg('retry', ['-retry', '-r'])
        ])

    @property
    def results_menu(self) -> str:
        raise NotImplementedError

    def validate_result_num(self, num:str) -> int:
        raise NotImplementedError

    def convert_num_to_name(self, num:int) -> str:
        raise NotImplementedError

    def print_search_view(self):
        return self.app.fetch_component('standard_page_component').print(
            page_content=_search_template,
            page_title='Ingredient Search'
        )

    def print_results_view(self):
        output = _results_template.format(
            results=self.results_menu
        )
        return self.app.fetch_component('standard_page_component').print(
            page_content=output,
            page_title='Ingredient Search Results'
        )


