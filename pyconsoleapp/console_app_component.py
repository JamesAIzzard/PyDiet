from abc import abstractmethod, ABC
from typing import Callable, Dict, Any, TYPE_CHECKING

from pyconsoleapp.console_app import ConsoleApp
from pinjector import inject

if TYPE_CHECKING:
    from pyconsoleapp import utility_service


class ConsoleAppComponent(ABC):
    def __init__(self):
        self.option_responses: Dict[str, Callable] = {}
        self.app: 'ConsoleApp' = inject('pyconsoleapp.app')

    def __getattribute__(self, name: str) -> Any:
        '''Intercepts the print command and adds the component to
        the app's list of active components.

        Arguments:
            name {str} -- Name of the attribute being accessed.

        Returns:
            Any -- The attribute which was requested.
        '''
        # If the print method was called;
        if name == 'print':
            # Add this component to the active components list
            self.app.activate_component(self)
        # Return whatever was requested;
        return super().__getattribute__(name)

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def print(self, *args, **kwargs) -> str:
        pass

    def set_option_response(self, signature: str, func: Callable) -> None:
        self.option_responses[signature] = func

    def dynamic_response(self, raw_response: str) -> None:
        pass

    def run(self) -> None:
        pass
