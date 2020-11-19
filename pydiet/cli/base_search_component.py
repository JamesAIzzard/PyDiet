import abc
from typing import Callable

from pyconsoleapp import Component
from pyconsoleapp import builtin_components


class BaseSearchComponent(Component, abc.ABC):
    """Abstract base class for search components. Used as a base class for a component which
    needs to search through persisted items by name."""

    _template = '''Search term: 
'''

    def __init__(self, on_result_selected: Callable[[str], None],
                 subject_type_name: str, **kwds):
        super().__init__(**kwds)

        self._subject_type_name: str = subject_type_name
        self._on_result_selected: Callable[[str], None] = on_result_selected  # Result selection handler.

        self._page_component = self.use_component(builtin_components.StandardPageComponent)
        self._page_component.configure(page_title='{} Search'.format(self._subject_type_name))

        self._results_component = self.delegate_state('results', BaseSearchResultsComponent)
        self._results_component.configure(on_back=self.get_state_changer('main'))

    def printer(self, **kwds) -> str:
        return self._page_component.printer(page_content=self._template)

class BaseSearchResultsComponent(Component):
    """Base class for search results components. Used to display search results and respond to result
    selection."""

    _template = '''Choose a result number to select.
'''

    def __init__(self, on_result_selected: Callable[[str], None], **kwds):
        super().__init__(**kwds)

        self._page_component = self.use_component(builtin_components.StandardPageComponent)
        self._page_component.configure(
            page_title='{} Search'.format(self._subject_type_name),
            go_back=self.get_state_changer('main')
        )
