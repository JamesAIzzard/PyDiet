from abc import abstractmethod, ABC
from typing import Callable, Dict, Any, TYPE_CHECKING

from pyconsoleapp.console_app import ConsoleApp
from pinjector import inject

if TYPE_CHECKING:
    from pyconsoleapp import utility_service


class ConsoleAppComponent(ABC):
    def __init__(self):
        self.option_responses: Dict[str, Callable] = {}
        self.app: 'ConsoleApp' = inject('cli.app')

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
            # Call the on_run method;
            self.run()
            # Add this component to the active components list
            # (Don't bring service onto scope, because some child is likely to
            # want to write to self._utility_service, overwriting it);
            utility_service:'utility_service' = inject('cli.utility_service')
            self.app.make_component_active(utility_service
                                           .pascal_to_snake(self.name))
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

    def dynamic_response(self, response: str) -> None:
        pass

    def run(self) -> None:
        pass

    def goto(self, route: str) -> None:
        self.app.goto(route)

    def get_component(self, component_name: str) -> 'ConsoleAppComponent':
        return self.app.get_component(component_name)

    def clear_entrance(self, route: str) -> None:
        self.app.clear_entrance(route)

    def clear_exit(self, route: str) -> None:
        self.app.clear_exit(route)

    def guard_entrance(self, route: str, component_name: str) -> None:
        self.app.guard_entrance(route, component_name)

    def guard_exit(self, route: str, component_name: str) -> None:
        self.app.guard_exit(route, component_name)
