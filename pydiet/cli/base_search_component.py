import abc
from collections import OrderedDict
from typing import List, Callable, Optional, Type, TYPE_CHECKING

from pyconsoleapp import Component, PrimaryArg, builtin_components
from pydiet import persistence

if TYPE_CHECKING:
    from pydiet.persistence import SupportsPersistence


class BaseSearchComponent(Component, abc.ABC):
    """Abstract base class for search components. Used as a base class for a component which
    needs to search through persisted items by name."""

    _template = '''Search term: \n'''

    def __init__(self, on_result_selected: Callable[[str], None], **kwds):
        super().__init__(**kwds)

        self._on_result_selected: Callable[[str], None] = on_result_selected

        # type: builtin_components.StandardPageComponent
        self._page_component = self.use_component(builtin_components.StandardPageComponent(
            page_title='{} Search'.format(self._subject_type_name)
        ))

        # type: SearchResultsComponent
        self._results_component = self.delegate_state('results', SearchResultsComponent(
            subject_type_name=self._subject_type_name(),
            on_result_selected=self._on_result_selected
        ))

        self.configure(responders=[
            self.configure_responder(self._on_search, args=[
                PrimaryArg(name='search_term', accepts_value=True, markers=None)
            ])
        ])

    @staticmethod
    @abc.abstractmethod
    def _subject_type() -> Type['SupportsPersistence']:
        """Returns the subject type the search component will deal with."""
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def _subject_type_name() -> str:
        """Returns the subject type's readable name."""
        raise NotImplementedError

    def _on_search(self, search_term: str) -> None:
        """Implements search of saved object names, based on the search_term."""
        results = persistence.search_for_names(self._subject_type(), search_term)
        self.load_results(results)
        self.current_state = 'results'

    def printer(self, **kwds) -> str:
        return self._page_component.printer(page_content=self._template)

    def load_results(self, results: List[str]) -> None:
        """Loads a list of results into the results-state component."""
        self._results_component.load_results(results)

    def configure(self, on_result_selected: Optional[Callable[[str], None]] = None, **kwds) -> None:
        super().configure(**kwds)
        if on_result_selected is not None:
            self._results_component.configure(on_result_selected=on_result_selected)


class SearchResultsComponent(Component):
    """Used to display search results and respond to result selection."""

    _template = '''
{results}
{single_hr}
Choose a result number.
'''

    def __init__(self, on_result_selected: Optional[Callable[[str], None]] = None, **kwds):
        super().__init__(**kwds)

        self._results: List[str] = []

        self._on_result_selected: Optional[Callable[[str], None]] = None
        if on_result_selected is not None:
            self._on_result_selected = on_result_selected

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

    def printer(self, **kwds) -> str:
        ...

    def load_results(self, results: List[str]) -> None:
        """Loads a list of results."""
        self._results = results

    def configure(self, on_result_selected: Optional[Callable[[str], None]] = None, **kwds) -> None:
        super().configure(**kwds)
        if on_result_selected is not None:
            self._on_result_selected = on_result_selected
