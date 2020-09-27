import abc
from typing import Callable, Any, Dict, Optional

import pyconsoleapp
from pyconsoleapp import ConsoleAppComponent

_search_screen_template = '''
------------------------|----------------------------
Search ->               | (enter)
------------------------|----------------------------

Enter {subject_name} name:'''

_results_screen_template = '''
------------------------|----------------------------
Select ->               | [result number]
------------------------|----------------------------

Results:
{search_results}
'''


class BaseSearchComponent(ConsoleAppComponent, abc.ABC):

    def __init__(self, app):
        super().__init__(app)
        self._subject_name: Optional[str] = None
        self._on_result_selected: Optional[Callable] = None
        self._results_num_map: Dict[int, str] = {}

        self.configure_state('search', self._print_search_screen, responders=[
            self.configure_responder(self._on_search, args=[
                pyconsoleapp.PrimaryArg('search_term', has_value=True, markers=None)])
        ])

        self.configure_state('results', self._print_results_screen, responders=[
            self.configure_responder(self._on_select_result, args=[
                pyconsoleapp.PrimaryArg('result_num', has_value=True, markers=None, validators=[
                    self._validate_result_num])])
        ])

    @property
    def _results_menu(self) -> str:
        results_menu = ''

        for result_num in self._results_num_map:
            result_name = self._result_name_from_num(result_num)
            results_menu = results_menu + '{num}. {result_name}\n'.format(
                num=result_num, result_name=result_name)
        return results_menu

    def _result_name_from_num(self, result_num: int) -> str:
        return self._results_num_map[result_num]

    def _print_search_screen(self) -> str:
        return self.app.get_component(pyconsoleapp.StandardPageComponent).print(
            page_title='{} Search'.format(self._subject_name.capitalize()),
            page_content=_search_screen_template.format(subject_name=self._subject_name.capitalize())
        )

    def _print_results_screen(self) -> str:
        results_screen = _results_screen_template.format(
            search_results=self._results_menu
        )
        return self.app.get_component(pyconsoleapp.StandardPageComponent).print(
            page_title='{} Search Results'.format(self._subject_name.capitalize()),
            page_content=results_screen
        )

    def _validate_result_num(self, value: Any) -> int:
        try:
            result_num = int(value)
        except ValueError:
            raise pyconsoleapp.ResponseValidationError('Please enter a valid result number.')
        if result_num not in self._results_num_map:
            raise pyconsoleapp.ResponseValidationError('{} does not refer to a result number.'.format(result_num))
        return result_num

    @abc.abstractmethod
    def _on_search(self, args) -> None:
        raise NotImplementedError

    def _on_select_result(self, args) -> None:
        self._on_result_selected(self._result_name_from_num(args['result_num']))

    def configure(self, subject_name: str, on_result_selected: Callable) -> None:
        self._subject_name = subject_name
        self._on_result_selected = on_result_selected

    def clear_results(self) -> None:
        self._results_num_map = {}
