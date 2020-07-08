from abc import abstractmethod, ABC
from typing import Callable, Dict, List, Any, TYPE_CHECKING

from pyconsoleapp.exceptions import (
    NoPrintFunctionError,
    StateNotConfiguredError
)

if TYPE_CHECKING:
    from pyconsoleapp import ConsoleApp


class ConsoleAppComponent(ABC):
    def __init__(self, app: 'ConsoleApp'):
        # Stash the app reference;
        self.app = app
        # Dicts to store state specific print & response funcs;
        self._sig_response_functions: Dict[str, Dict[str, Dict]] = {}
        self._any_response_functions: Dict[str, Callable] = {}
        self._print_functions: Dict[str, Callable] = {}
        # Configure the states;
        self._states: List[str] = ['DEFAULT']
        self._state: str = self._states[0]

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

    @property
    def state(self) -> str:
        return self._state

    @state.setter
    def state(self, value:str) -> None:
        if not value in self._states:
            raise StateNotConfiguredError
        self._state = value

    def print(self, *args, **kwargs) -> str:
        # Check the current state has a print function assigned;
        if not self.state in self._print_functions.keys():
            raise NoPrintFunctionError
        # Run the function;
        return self._print_functions[self._state](args, kwargs)

    def respond(self, response:str)->None:
        # Check the any-response function for this state;
        if self.state in self._any_response_functions.keys():
            self._any_response_functions[self.state](response)
        # Check if the component finalised response;
        if self.app._stop_responding:
            return
        # Check each signature response stored against this state;
        for sig in self._sig_response_functions[self.state].keys():
            # Handle an empty response;
            if response.replace(' ', '') == '':
                if '' in self._sig_response_functions[self.state].keys():
                    self._sig_response_functions[self.state]['']()
            # Parse the response, looking for signature;
            # Split into chunks;
            # Search for flags;   

    def configure_states(self, states: List[str]):
        # Prevent default being overwritten by no states;
        if len(states):
            # Assign states;
            self._states = states
            # Init the current state as the first one;
            self.state = states[0]
            # Remove the default states from the print and response dicts;
            self._print_functions = {}
            self._sig_response_functions = {}
            self._any_response_functions = {}

    def validate_state(self, state:str)->None:
        if not state in self._states:
            raise StateNotConfiguredError

    def set_print_function(
            self,
            func: Callable,
            states: List[str] = []) -> None:
        # If no state was specified;
        if not len(states):
            # If no states have been configured;
            if self.states == ['DEFAULT']:
                # Assign to default;
                self._print_functions['DEFAULT'] = func
            # If states have been configured;
            else:
                # Assign print function to each state;
                for state in self._states:
                    self._print_functions[state] = func
        # If state(s) were specified;
        elif len(states):
            # Cycle through each specified state;
            for state in states:
                # Check it exists;
                self.validate_state(state)
                # Assign the function to the state;
                self._print_functions[state] = func

    def set_response_function(
            self,
            signatures: List[str],
            func: Callable,
            states: List[str] = [],
            exact: bool = False) -> None:
        # If no state was specified;
        if not len(states):
            # If no states have been configured;
            if self.states == ['DEFAULT']:
                # Assign to default;
                self._sig_response_functions['DEFAULT'] = {
                    'exact': exact,
                    'func': func
                }
            # If states have been configured;
            else:
                # Assign to every state;
                for state in self._states:
                    self._sig_response_functions[state] = {
                        'exact': exact,
                        'func': func
                    }
        # If state(s) were specified;
        elif len(states):
            # Cycle through each specifed state;
            for state in states:
                # Check it exists;
                self.validate_state(state)
                # Assign the function to the state;
                self._sig_response_functions[state] = {
                    'exact': exact,
                    'func': func
                }

    def set_empty_response_function(
            self,
            func: Callable,
            states: List[str] = []) -> None:
        self.set_response_function([''], func, states=states, exact=True)

    def set_any_response_function(
        self,
        func: Callable,
        states: List[str] = []) -> None:
        # If no state was specified;
        if not len(states):
            # If no states have been configured;
            if self.states == ['DEFAULT']:
                # Assign to default;
                self._any_response_functions['DEFAULT'] = func
            # If states have been configured;
            else:
                # Assign to every state;
                for state in self._states:
                    self._any_response_functions[state] = func
        # If states were specified;
        elif len(states):
            # Cycle through each specified state;
            for state in states:
                # Check the state exists;
                self.validate_state(state)
                # Assign the function to the state;
                self._any_response_functions[state] = func


    def before_print(self) -> None:
        pass


class ConsoleAppGuardComponent(ConsoleAppComponent):
    def __init__(self, app: 'ConsoleApp'):
        super().__init__(app)

    def clear_self(self):
        def search_and_clear_guard_map(guard_map):
            # Place to store guarded route to clear;
            rt_to_clear = None
            # Work through the entrance guard list looking for self;
            for route in guard_map.keys():
                # If found;
                if guard_map[route] == self:
                    # Delete entry from guard dict;
                    rt_to_clear = route
            if rt_to_clear:
                del guard_map[rt_to_clear]
        # Search and clear entrance & exit maps;
        search_and_clear_guard_map(self.app._route_entrance_guard_map)
        search_and_clear_guard_map(self.app._route_exit_guard_map)
