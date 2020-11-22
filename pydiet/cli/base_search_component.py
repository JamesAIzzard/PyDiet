import abc
from collections import OrderedDict
from typing import List, Callable, Optional

from pyconsoleapp import Component
from pyconsoleapp import builtin_components


class BaseSearchComponent(Component, abc.ABC):
    """Abstract base class for search components. Used as a base class for a component which
    needs to search through persisted items by name."""

    _template = '''Search term: 
'''

    def __init__(self, **kwds):
        super().__init__(**kwds)

        self._subject_type_name: Optional[str] = None

        self._page_component = self.use_component(builtin_components.StandardPageComponent)
        self._page_component.configure(page_title='{} Search'.format(self._subject_type_name))

        self._results_component = self.delegate_state('results', BaseSearchResultsComponent)
        self._results_component._subject_type_name = self._subject_type_name

    def printer(self, **kwds) -> str:
        return self._page_component.printer(page_content=self._template)

    def load_results(self, results: List[str]) -> None:
        """Loads a list of results into the results-state component."""
        self._results_component.load_results(results)

    def configure(self, on_result_selected: Optional[Callable[[str], None]] = None, **kwds) -> None:
        super().configure(**kwds)
        if on_result_selected is not None:
            self._results_component.configure(on_result_selected=on_result_selected)


class BaseSearchResultsComponent(Component, abc.ABC):
    """Base class for search results components. Used to display search results and respond to result
    selection."""

    _template = '''
{results}
{single_hr}
Choose a result number.
'''

    def __init__(self, **kwds):
        super().__init__(**kwds)

        self._results: List[str] = []
        self._on_result_selected: Optional[Callable[[str], None]] = None

        self._subject_type_name: Optional[str] = None
        self._page_component = self.use_component(builtin_components.StandardPageComponent)
        self._page_component.configure(
            page_title='{} Search'.format(self._subject_type_name),
            go_back=self.get_state_changer('main')
        )

    @property
    def _results_num_map(self) -> OrderedDict[int, str]:
        """Returns a dictionary of the results, associated with incrementing integer numbers."""
        output = OrderedDict()
        for i, result_name in enumerate(self._results, start=1):
            output[i] = result_name
        return output

    @property
    def _numbered_results(self) -> str:
        """Returns a newline seperated string of numbered results."""
        _template = '{num}.:<4 {result_name}\n'
        output = ''
        for num, result_name in self._results_num_map.items():
            output = output + _template.format(num=num, result_name=result_name)
        return output

    def load_results(self, results: List[str]) -> None:
        """Loads a list of results."""
        self._results = results

    def configure(self, on_result_selected: Optional[Callable[[str], None]] = None, **kwds) -> None:
        super().configure(**kwds)
        if on_result_selected is not None:
            self._on_result_selected = on_result_selected
