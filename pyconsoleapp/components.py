from abc import ABC
from inspect import signature
from pyconsoleapp.exceptions import PyConsoleAppError
from typing import Callable, Dict, List, Tuple, Any, Optional, Union, TYPE_CHECKING, cast

from pyconsoleapp import ConsoleApp, exceptions

if TYPE_CHECKING:
    from pyconsoleapp import ConsoleApp


class Responder():
    def __init__(self,
                 app: 'ConsoleApp',
                 func: Callable,
                 args: List['ResponderArg']):
        self._app = app
        self._func = func
        self._args = args

        # Check there are not multiple markerless args within this responder;
        markerless_found = False
        for arg in args:
            if arg.is_markerless:
                if not markerless_found:
                    markerless_found = True
                else:
                    raise exceptions.DuplicateMarkerlessArgError

        # Check there is at least one primary arg within this responder;
        primary_found = False
        for arg in args:
            if arg.primary:
                primary_found = True
        if not primary_found:
            raise exceptions.NoPrimaryArgError

        # Check there are no primary marker clashes within this responder;
        primary_markers = []
        for arg in args:
            if arg.primary:
                for marker in arg.markers:
                    if marker in primary_markers:
                        raise exceptions.DuplicatePrimaryMarkerError
                    primary_markers.append(marker)

    @property
    def app(self) -> 'ConsoleApp':
        return self._app

    @property
    def args(self) -> List['ResponderArg']:
        return self._args

    @property
    def is_argless_responder(self) -> bool:
        if len(self.args) == 0:
            return True
        return False

    @property
    def has_markerless_arg(self) -> bool:
        if not self.is_argless_responder:
            for arg in self.args:
                if None in arg.markers:
                    return True
        return False

    @property
    def markerless_arg(self) -> Optional['ResponderArg']:
        if self.has_markerless_arg:
            for arg in self.args:
                if arg.is_markerless:
                    return arg
        return None

    @property
    def primary_markers(self) -> List[str]:
        all_primary_markers = []
        for arg in self.args:
            if arg.primary:
                all_primary_markers = all_primary_markers+arg.markers
        return all_primary_markers

    def check_response_match(self, response: str) -> bool:
        '''Returns True/False to indicate if all of the primary
        argument markers are present in the response.

        Args:
            response (str): Text entered by user.

        Returns:
            bool: To indicate match or no match.
        '''
        for arg in self.args:
            if arg.primary:
                if not arg.check_marker_match(response):
                    return False
        return True

    def parse_response_to_args(self, response: str) -> Dict[str, Any]:
        '''Returns dict of all possible arg names, with None as value if arg
        was not present.
        - Valueless arg values are True if present, False if not.
        - Sequentially passes values through any validation functions.

        Args:
            response (str): [description]

        Returns:
            Dict[str, Any]: [description]
        '''

        # First check that all primary arg markers are present;
        for arg in self.args:
            if arg.primary:
                if not arg.check_marker_match(response):
                    raise exceptions.ArgMissingValueError(
                        'Trying to parse a response which is missing some primary args.')

        # Place to store arg names found in the response;
        matched_arg_names: List[str] = []
        # Final arg dict we will ultimately return;
        parsed_args: Dict[str, Any] = {}

        # Init values as False if valueless, default if available and None otherwise;
        for arg in self.args:
            if arg.is_valueless:
                parsed_args[arg.name] = False
            else:
                if not arg.default_value == None:
                    parsed_args[arg.name] = arg.default_value
                else:
                    parsed_args[arg.name] = None

        # Split the response into list so we can work through each word;
        words = response.split()

        # Init the first arg name;
        if self.has_markerless_arg:
            current_arg_name = self.markerless_arg.name
        else:
            current_arg_name = None

        # Now cycle through each word in the response;
        for word in words:
            # Check if the word is a marker;
            is_marker = False
            for arg in self.args:
                if word in arg.markers:
                    matched_arg_names.append(arg.name)
                    current_arg_name = arg.name
                    is_marker = True
                    # If the arg is valueless, adjust value to indicate it was found;
                    if arg.is_valueless:
                        parsed_args[arg.name] = True
                        current_arg_name = None
                    break  # Found, so stop searching args.
            # Append value if not a marker, and an arg is collecting a value;
            if not is_marker:
                # If we are getting a value before a marker, it is an orphan;
                if current_arg_name == None:
                    raise exceptions.OrphanValueError('Unexpected argument: {}'.format(word))
                # If the word is the first for this value, init;
                if parsed_args[current_arg_name] == None:
                    parsed_args[current_arg_name] = word
                # Otherwise append;
                else:
                    parsed_args[current_arg_name] = '{} {}'.format(
                        parsed_args[current_arg_name], word)

        # Run validation over each arg;
        for arg in self.args:
            # Flag any None primary values;
            if arg.primary and parsed_args[arg.name] == None:
                raise exceptions.ArgMissingValueError('{arg_name} requires a value.'.format(
                    arg_name=arg.name))
            # If the value is not none, pass it through any validators assigned;
            if not parsed_args[arg.name] == None:
                for validator in arg.validators:
                    parsed_args[arg.name] = validator(parsed_args[arg.name])

        return parsed_args

    def __call__(self, response: str = '') -> None:
        # Parse the response into args;
        args = self.parse_response_to_args(response)
        # Ready to go, assume stop responding after this;
        # (Component can undo this if it wants to continue the
        # response cycle).
        self._app.stop_responding()
        # Call the function, passing the args if the function expects them;
        sig = signature(self._func)
        if len(sig.parameters) > 0:
            self._func(args)
        else:
            self._func()


class ResponderArg():
    def __init__(self,
                 primary: bool,
                 valueless: bool,
                 name: str,
                 markers: List[Union[str, None]],
                 validators: List[Callable] = [],
                 default_value: Any = None):
        self._primary = primary
        self._valueless = valueless
        self._name = name
        self._markers = markers
        self._validators = validators
        self._default_value = default_value

        # Check the default value passes validation if it has
        # been set;
        if not default_value == None:
            try:
                for validator in self.validators:
                    self._default_value = validator(self._default_value)
            except exceptions.ResponseValidationError:
                raise ValueError('The default value fails validation')

    def check_marker_match(self, response: str) -> bool:
        '''Returns True/False to indicate if markers for this argument
        are present in the response.

        Args:
            response (str): Response to search for arguments.

        Returns:
            bool: To indicate if a marker was found.
        '''
        chunked_response = response.split()
        for marker in self.markers:
            if marker in chunked_response or marker == None:
                return True
        return False

    @property
    def primary(self) -> bool:
        return self._primary

    @property
    def name(self) -> str:
        return self._name

    @property
    def markers(self) -> List[Union[str, None]]:
        return self._markers

    @property
    def validators(self) -> List[Callable]:
        return self._validators

    @property
    def default_value(self) -> Any:
        return self._default_value

    @property
    def is_markerless(self) -> bool:
        if None in self.markers:
            return True
        else:
            return False

    @property
    def is_valueless(self) -> bool:
        return self._valueless


class ConsoleAppComponent(ABC):
    def __init__(self, app: 'ConsoleApp'):
        # Stash the app reference;
        self.app = app
        # Dicts to store state specific print & responder funcs;
        self._responders: Dict[Union[None, str],
                               List['Responder']] = {None: []}
        self._printers: Dict[Union[None, str], Callable] = {}
        # Init state storage;
        self._states: List[Union[None, str]] = [None]
        self._current_state: Union[None, str] = self._states[0]

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
        '''Returns the name of the component.

        Returns:
            str: Component name.
        '''
        return self.__class__.__name__

    @property
    def current_state(self) -> Union[None, str]:
        return self._current_state

    @current_state.setter
    def current_state(self, value: Union[None, str]) -> None:
        self._validate_states([value])
        self._current_state = value

    @property
    def states(self) -> List[Union[None, str]]:
        return self._states

    def configure_states(self, states: List[Union[None, str]]) -> None:
        # Prevent default being overwritten by no states;
        if len(states):
            # Reset to remove the None state;
            self._states = []
            self._responders = {}
            # Assign states;
            for state in states:
                self._states.append(state)
                self._responders[state] = []
            # Init the current state as the first one;
            self.current_state = states[0]
        else:
            raise ValueError('At least one state must be provided.')

    def _validate_states(self, states: List[Union[None, str]]):
        # Check that each state in the list has been configured;
        for state in states:
            if not state in self.states:
                raise exceptions.StateNotFoundError

    def change_state(self, state:str)->Callable:
        # Check the state is real;
        self._validate_states([state])
        # Create the callable;
        def state_changer():
            self.current_state = state
        return state_changer

    @property
    def _current_print_function(self) -> Callable:
        # Error if there isn't a print function stored against the current state;
        if not self.current_state in self._printers.keys():
            raise exceptions.NoPrintFunctionError
        # Return the relevant function;
        return self._printers[self.current_state]

    def print(self, *args, **kwargs) -> Union[str, Tuple[str, str]]:
        return self._current_print_function(*args, **kwargs)

    def before_print(self) -> None:
        pass

    def configure_printer(self,
                          func: Callable,
                          states: List[Union[str, None]] = [None]) -> None:
        # Check all the states;
        self._validate_states(states)
        # Assign the print function to specified states;
        for state in states:
            self._printers[state] = func

    def configure_responder(self,
                            func: Callable,
                            states: List[Union[str, None]] = [None],
                            args: List['ResponderArg'] = []) -> None:
        '''Generic responder configuration. 

        Args:
            func (Callable): Handler function to execute when the responder is called.
            states (List[Union[str, None]]): The component states under which the responder
                can be called. Defaults to [None].
            args (List[ResponderArg]): The responder args associated with the responder.
                The contents of these args are passed to the function as a dict, when the
                responder is called. Defaults to None.
        '''
        # Check the states are valid;
        self._validate_states(states)

        # If this is an empty responder, check there are no others;
        if len(args) == 0:
            for responder in self._responders[self.current_state]:
                if responder.is_argless_responder:
                    raise exceptions.DuplicateEmptyResponderError

        # Check the primary markers in this responder don't collide
        # with any that have been configured in this state already;
        for marker in self.get_primary_markers(states):
            for arg in args:
                if marker in arg.markers:
                    raise exceptions.DuplicatePrimaryMarkerError

        # Create and stash the responder object in the correct states;
        r = Responder(self.app, func, args)
        for state in states:
            self._responders[state].append(r)

    @staticmethod
    def configure_std_primary_arg(name: str,
                                  markers: List[Union[str, None]] = [],
                                  validators: List[Callable] = [],
                                  default_value: Any = None) -> 'ResponderArg':
        '''Configures a primary argument object, describing how input is collected
        and validated against an argument to be passed to the handler function.
        'Primary' indicates the argument must be present for the responder to
        match and be called. In the case where the name parameter == None, the argument
        will not contribute values to the arg dict passed to the handler function.

        Returns:
            ResponderArg
        '''
        return ResponderArg(primary=True, valueless=False, name=name, markers=markers,
                            validators=validators, default_value=default_value)

    @staticmethod
    def configure_markerless_primary_arg(name: str,
                                         validators: List[Callable] = [],
                                         default_value: Any = None) -> 'ResponderArg':
        '''Configures a primary argument object without a marker, i.e one whose value
        is the text entered before the first marker found in the response.

        Returns:
            ResponderArg
        '''
        return ResponderArg(primary=True, valueless=False, markers=[None],
                            name=name, validators=validators, default_value=default_value)

    @staticmethod
    def configure_valueless_primary_arg(name: str,
                                        markers: List[str]) -> 'ResponderArg':
        '''Configures a primary argument object which only looks for a marker and no
        additional arguments.

        Returns:
            ResponderArg
        '''
        if None in markers:
            raise ValueError('Valueless args cannot have None as a marker')
        return ResponderArg(primary=True, valueless=True,
                            markers=cast(List[Union[str, None]], markers), name=name)

    @staticmethod
    def configure_std_option_arg(name: str,
                                 markers: List[Union[str, None]] = [],
                                 validators: List[Callable] = [],
                                 default_value: Any = None) -> 'ResponderArg':
        '''Configures an optional argument object, describing how input is collected
        and validated against an argument to be passed to the handler function.
        'Option' indicates the argument must be present for the responder to
        match and be called. In the case where the name parameter == None, the argument
        will not contribute values to the arg dict passed to the handler function.

        Returns:
            ResponderArg
        '''
        return ResponderArg(primary=False, valueless=False, name=name, markers=markers,
                            validators=validators, default_value=default_value)

    @staticmethod
    def configure_markerless_option_arg(name: str,
                                        validators: List[Callable] = [],
                                        default_value: Any = None) -> 'ResponderArg':
        '''Configures an option argument object without a marker, i.e one whose value
        is the text entered before the first marker found in the response.

        Returns:
            ResponderArg
        '''
        return ResponderArg(primary=False, valueless=False, markers=[None],
                            name=name, validators=validators, default_value=default_value)

    @staticmethod
    def configure_valueless_option_arg(name: str,
                                       markers: List[str]) -> 'ResponderArg':
        '''Configures an option argument object which only looks for a marker and no
        additional arguments.

        Returns:
            ResponderArg
        '''
        if None in markers:
            raise ValueError('Valueless args cannot have None as a marker')
        return ResponderArg(primary=False, valueless=True,
                            markers=cast(List[Union[str, None]], markers), name=name)

    def configure_argless_responder(self,
                                    func: Callable,
                                    states: List[Union[str, None]] = [None]) -> None:
        '''A shortcut method to configure a responder to fire when the
        user presses enter without entering anything.

        Args:
            func (Callable): Function to call when responder is matched.
            states (List[Union[str, None]], optional): Component states from which the responder 
                can be called. Defaults to [None].
        '''
        # Go ahead and configure a responder without args;
        self.configure_responder(func, states)

    @property
    def argless_responder(self) -> Optional['Responder']:
        '''Returns the argless responder assigned to the component,
        if it exists. If there is no argless responder configured,
        None is returned.

        Returns:
            Responder | None
        '''
        for responder in self._responders[self.current_state]:
            if responder.is_argless_responder:
                return responder
        return None

    @property
    def marker_responders(self) -> List['Responder']:
        '''Returns a list of responders whose arguments are
        each assigned a marker.

        Returns:
            List[Responder]
        '''
        marker_responders = []
        for responder in self._responders[self.current_state]:
            if not responder.is_argless_responder and not responder.has_markerless_arg:
                marker_responders.append(responder)
        return marker_responders

    @property
    def markerless_responder(self) -> Optional['Responder']:
        '''Returns the markerless responder assigned to the component,
        if it exists. If there is no markerless responder configured,
        None is returned.

        A markerless responder is a responder containing an argument
        with its marker set as None. This means it will match against
        any input preceeding the first marker found in the response.

        Returns:
            Responder | None
        '''
        for responder in self._responders[self.current_state]:
            if responder.has_markerless_arg:
                return responder
        return None

    def get_primary_markers(self, states: List[Union[str, None]]) -> List['str']:
        '''Returns a list of all primary markers for the list of states 
        specified.'''
        all_markers = []
        for state in states:
            for responder in self._responders[state]:
                for arg in responder.args:
                    if arg.primary:
                        all_markers = all_markers+arg.markers
        return all_markers


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
