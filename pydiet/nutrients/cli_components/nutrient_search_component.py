from typing import Callable, Any, Dict, Optional

from pyconsoleapp import ConsoleAppComponent, PrimaryArg, ResponseValidationError, search_tools, menu_tools, \
    StandardPageComponent
from pydiet import nutrients

_search_screen_template = '''
------------------------|----------------------------
Search ->               | (enter)
------------------------|----------------------------

Enter nutrient name:'''

_results_screen_template = '''
------------------------|----------------------------
Select ->               | [result number]
------------------------|----------------------------

Results:
{search_results}
'''


class NutrientSearchComponent(ConsoleAppComponent):

    def __init__(self, app):
        super().__init__(app)
        self._on_nutrient_selected: Optional[Callable] = None
        self._results_num_map: Dict[int, str] = {}

        self.configure_state('search', self._print_search_screen, responders=[
            self.configure_responder(self._on_search, args=[
                PrimaryArg('search_term', has_value=True, markers=None)])
        ])

        self.configure_state('results', self._print_results_screen, responders=[
            self.configure_responder(self._on_select_result, args=[
                PrimaryArg('result_num', has_value=True, markers=None, validators=[
                    self._validate_result_num])])
        ])

    @property
    def _results_menu(self) -> str:
        results_menu = ''

        for result_num in self._results_num_map:
            result_name = self._result_name_from_num(result_num)
            alias_summary = ''
            primary_name = nutrients.nutrients_service.get_nutrient_primary_name(result_name)
            if not primary_name == result_name:
                alias_summary = ' (alias for {})'.format(primary_name)
            results_menu = results_menu + '{num}. {nutrient_name}{alias_summary}\n'.format(
                num=result_num, nutrient_name=result_name, alias_summary=alias_summary
            )
        return results_menu

    def _result_name_from_num(self, result_num: int) -> str:
        return self._results_num_map[result_num]

    def _print_search_screen(self) -> str:
        return self.app.get_component(StandardPageComponent).print(
            page_title='Nutrient Search',
            page_content=_search_screen_template
        )

    def _print_results_screen(self) -> str:
        results_screen = _results_screen_template.format(
            search_results=self._results_menu
        )
        return self.app.get_component(StandardPageComponent).print(
            page_title='Nutrient Search Results',
            page_content=results_screen
        )

    def _validate_result_num(self, value: Any) -> int:
        try:
            result_num = int(value)
        except ValueError:
            raise ResponseValidationError('Please enter a valid result number.')
        if result_num not in self._results_num_map:
            raise ResponseValidationError('{} does not refer to a result number.'.format(result_num))
        return result_num

    def _on_search(self, args) -> None:
        results = search_tools.search_n_best_matches(
            nutrients.nutrients_service.all_primary_and_alias_nutrient_names(),
            args['search_term'], 5)
        self._results_num_map = menu_tools.create_number_name_map(results)
        self.change_state('results')

    def _on_select_result(self, args) -> None:
        self._on_nutrient_selected(self._result_name_from_num(args['result_num']))

    def configure(self, on_nutrient_selected: Callable) -> None:
        self._on_nutrient_selected = on_nutrient_selected

    def clear_results(self) -> None:
        self._results_num_map = {}
