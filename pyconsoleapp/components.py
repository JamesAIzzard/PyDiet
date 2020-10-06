from abc import ABC
from inspect import signature
from typing import Callable, Dict, List, Tuple, Any, Optional, Union, TYPE_CHECKING

from pyconsoleapp import ConsoleApp, exceptions

if TYPE_CHECKING:
    from pyconsoleapp import ConsoleApp


class Responder:
    def __init__(self,
                 app: 'ConsoleApp',
                 func: Callable,
                 args: List['ResponderArg'] = None):
        self._app = app
        self._func = func
        self._args = args

        if args is None:
            args = []

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
                        raise exceptions.IdenticalPrimaryMarkersError
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
                all_primary_markers = all_primary_markers + arg.markers
        return all_primary_markers

    def check_response_match(self, response: str) -> bool:
        """Returns True/False to indicate if all of the primary
        argument markers are present in the response.

        Args:
            response (str): Text entered by user.

        Returns:
            bool: To indicate match or no match.
        """
        for arg in self.args:
            if arg.primary:
                if not arg.check_marker_match(response):
                    return False
        return True

    def parse_response_to_args(self, response: str) -> Dict[str, Any]:
        """Returns dict of all possible arg names, with None as value if arg
        was not present.
        - Valueless arg values are True if present, False if not.
        - Sequentially passes values through any validation functions.

        Args:
            response (str): [description]

        Returns:
            Dict[str, Any]: [description]
        """

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
                if arg.default_value is not None:
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
                if current_arg_name is None:
                    raise exceptions.OrphanValueError('Unexpected argument: {}'.format(word))
                # If the word is the first for this value, init;
                if parsed_args[current_arg_name] is None:
                    parsed_args[current_arg_name] = word
                # Otherwise append;
                else:
                    parsed_args[current_arg_name] = '{} {}'.format(
                        parsed_args[current_arg_name], word)

        # Run validation over each arg;
        for arg in self.args:
            # Flag any None primary values;
            if arg.primary and parsed_args[arg.name] is None:
                raise exceptions.ArgMissingValueError('{arg_name} requires a value.'.format(
                    arg_name=arg.name))
            # If the value is not none, pass it through any validators assigned;
            if not parsed_args[arg.name] is None:
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


def PrimaryArg(arg_name: str, has_value: bool, markers: Optional[List[str]] = None,
               validators: List[Callable] = None, default_value=None) -> 'ResponderArg':
    if markers is None:
        markers = [None]
    if validators is None:
        validators = []
    return ResponderArg(primary=True, valueless=not has_value, name=arg_name, markers=markers, validators=validators,
                        default_value=default_value)


def OptionArg(arg_name: str, has_value: bool, markers: List[str] = None,
              validators: List[Callable] = None, default_value=None) -> 'ResponderArg':
    if markers is None:
        markers = []
    if validators is None:
        validators = []
    return ResponderArg(primary=False, valueless=not has_value, name=arg_name, markers=markers, validators=validators,
                        default_value=default_value)


class ResponderArg:
    def __init__(self,
                 primary: bool,
                 valueless: bool,
                 name: str,
                 markers: List[Union[str, None]],
                 validators=None,
                 default_value: Any = None):
        if validators is None:
            validators = []
        self._primary = primary
        self._valueless = valueless
        self._name = name
        self._markers = markers
        self._validators = validators
        self._default_value = default_value

        # Check the default value passes validation if it has
        # been set;
        if default_value is not None:
            try:
                for validator in self.validators:
                    self._default_value = validator(self._default_value)
            except exceptions.ResponseValidationError:
                raise ValueError('The default value fails validation')

    def check_marker_match(self, response: str) -> bool:
        """Returns True/False to indicate if markers for this argument
        are present in the response.

        Args:
            response (str): Response to search for arguments.

        Returns:
            bool: To indicate if a marker was found.
        """
        chunked_response = response.split()
        for marker in self.markers:
            if marker in chunked_response or marker is None:
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
        self._current_state: Union[None, str] = None

    def __getattribute__(self, name: str) -> Any:
        """Intercepts the print command and adds the component to
        the app's list of active components.

        Arguments:
            name -- Name of the attribute being accessed.

        Returns:
            The attribute which was requested.
        """
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
    def current_state(self) -> Union[None, str]:
        if self._current_state is None:
            self._current_state = self.states[0]
            return self._current_state
        else:
            return self._current_state

    @current_state.setter
    def current_state(self, value: Union[None, str]) -> None:
        self._validate_states([value])
        self._current_state = value

    def change_state(self, state_name: str) -> None:
        """Changes the component's current state."""
        self._validate_states([state_name])
        self._current_state = state_name

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
            if state not in self.states:
                raise exceptions.StateNotFoundError

    def make_state_changer(self, state: str) -> Callable:
        # Check the state is real;
        self._validate_states([state])

        # Create the callable;
        def state_changer():
            self.current_state = state

        return state_changer

    @property
    def _current_print_function(self) -> Callable:
        # Error if there isn't a print function stored against the current state;
        if self.current_state not in self._printers.keys():
            raise exceptions.NoPrintFunctionError
        # Return the relevant function;
        return self._printers[self.current_state]

    def print(self, *args, **kwargs) -> Union[str, Tuple[str, str]]:
        return self._current_print_function(*args, **kwargs)

    def before_print(self) -> None:
        pass

    def _before_print(self) -> None:
        pass

    def _on_load(self) -> None:
        pass

    def configure_printer(self,
                          func: Callable,
                          states=None) -> None:
        # Check all the states;
        if states is None:
            states = [None]
        self._validate_states(states)
        # Assign the print function to specified states;
        for state in states:
            self._printers[state] = func

    def configure_state(self, state_name: str, print_function: Callable, responders: List[Responder]) -> None:
        # Add the state to the state list, resetting from start value if rqd. Also reset responders list;
        if self.states == [None]:
            self._states = []
            self._responders = {}
        self._states = self._states + [state_name]
        # Add the printer;
        self._printers[state_name] = print_function
        # Init the state entry on the responders dict;
        if state_name not in self._responders:
            self._responders[state_name] = []
        # Add the responders;
        for responder in responders:
            self._responders[state_name].append(responder)

    def configure_responder(self,
                            func: Callable,
                            states=None,
                            args=None) -> 'Responder':
        """Generic responder configuration.

        Args:
            func (Callable): Handler function to execute when the responder is called.
            states (List[Union[str, None]]): The component states under which the responder
                can be called. Defaults to [None].
            args (List[ResponderArg]): The responder args associated with the responder.
                The contents of these args are passed to the function as a dict, when the
                responder is called. Defaults to None.
        """
        # Check the states are valid;
        if args is None:
            args = []
        if states is None:
            states = [None]

        # Nasty hack to make the new notation work;
        if states == [None] and None not in self.states:
            states = ['_temp']
            self._responders['_temp'] = []

        # If this is an empty responder, check there are no others;
        if len(args) == 0:
            for responder in self._responders[self.current_state]:
                if responder.is_argless_responder:
                    raise exceptions.DuplicateEmptyResponderError

        # Check the primary markers in this responder aren't identical to another set in this state;
        new_primary_markers = []
        for arg in args:
            if arg.primary:
                for marker in arg.markers:
                    new_primary_markers.append(marker)
        if not states == ['_temp']:  # More of the same nasty hack to allow the new configuration method;
            for s in states:
                respdrs = self._responders[s]
                for respdr in respdrs:
                    p_args = respdr.primary_markers
                    if new_primary_markers == p_args:
                        raise exceptions.IdenticalPrimaryMarkersError(str(p_args))

        # Create and stash the responder object in the correct states;
        r = Responder(self.app, func, args)

        # Assign the responders to the states;
        for state in states:
            self._responders[state].append(r)

        return r

    @staticmethod
    def configure_std_primary_arg(name: str,
                                  markers=None,
                                  validators=None,
                                  default_value: Any = None) -> 'ResponderArg':
        """Configures a primary argument object, describing how input is collected
        and validated against an argument to be passed to the handler function.
        'Primary' indicates the argument must be present for the responder to
        match and be called. In the case where the name parameter == None, the argument
        will not contribute values to the arg dict passed to the handler function.

        Returns:
            ResponderArg
        """
        if validators is None:
            validators = []
        if markers is None:
            markers = []
        return ResponderArg(primary=True, valueless=False, name=name, markers=markers,
                            validators=validators, default_value=default_value)

    @staticmethod
    def configure_markerless_primary_arg(name: str,
                                         validators=None,
                                         default_value: Any = None) -> 'ResponderArg':
        """Configures a primary argument object without a marker, i.e one whose value
        is the text entered before the first marker found in the response.

        Returns:
            ResponderArg
        """
        if validators is None:
            validators = []
        return ResponderArg(primary=True, valueless=False, markers=[None],
                            name=name, validators=validators, default_value=default_value)

    @staticmethod
    def configure_valueless_primary_arg(name: str,
                                        markers: List[str]) -> 'ResponderArg':
        """Configures a primary argument object which only looks for a marker and no
        additional arguments.

        Returns:
            ResponderArg
        """
        if None in markers:
            raise ValueError('Valueless args cannot have None as a marker')
        return ResponderArg(primary=True, valueless=True,
                            markers=markers, name=name)

    @staticmethod
    def configure_std_option_arg(name: str,
                                 markers=None,
                                 validators=None,
                                 default_value: Any = None) -> 'ResponderArg':
        """Configures an optional argument object, describing how input is collected
        and validated against an argument to be passed to the handler function.
        'Option' indicates the argument must be present for the responder to
        match and be called. In the case where the name parameter == None, the argument
        will not contribute values to the arg dict passed to the handler function.

        Returns:
            ResponderArg
        """
        if validators is None:
            validators = []
        if markers is None:
            markers = []
        return ResponderArg(primary=False, valueless=False, name=name, markers=markers,
                            validators=validators, default_value=default_value)

    @staticmethod
    def configure_markerless_option_arg(name: str,
                                        validators=None,
                                        default_value: Any = None) -> 'ResponderArg':
        """Configures an option argument object without a marker, i.e one whose value
        is the text entered before the first marker found in the response.

        Returns:
            ResponderArg
        """
        if validators is None:
            validators = []
        return ResponderArg(primary=False, valueless=False, markers=[None],
                            name=name, validators=validators, default_value=default_value)

    @staticmethod
    def configure_valueless_option_arg(name: str,
                                       markers: List[str]) -> 'ResponderArg':
        """Configures an option argument object which only looks for a marker and no
        additional arguments.

        Returns:
            ResponderArg
        """
        if None in markers:
            raise ValueError('Valueless args cannot have None as a marker')
        return ResponderArg(primary=False, valueless=True,
                            markers=markers, name=name)

    def configure_argless_responder(self,
                                    func: Callable,
                                    states=None) -> None:
        """A shortcut method to configure a responder to fire when the
        user presses enter without entering anything.

        Args:
            func (Callable): Function to call when responder is matched.
            states (List[Union[str, None]], optional): Component states from which the responder
                can be called. Defaults to [None].
        """
        if states is None:
            states = [None]
        # Go ahead and configure a responder without args;
        self.configure_responder(func, states)

    @property
    def argless_responder(self) -> Optional['Responder']:
        """Returns the argless responder assigned to the component,
        if it exists. If there is no argless responder configured,
        None is returned.

        Returns:
            Responder | None
        """
        for responder in self._responders[self.current_state]:
            if responder.is_argless_responder:
                return responder
        return None

    @property
    def marker_responders(self) -> List['Responder']:
        """Returns a list of responders whose arguments are
        each assigned a marker.

        Returns:
            List[Responder]
        """
        marker_responders = []
        for responder in self._responders[self.current_state]:
            if not responder.is_argless_responder and not responder.has_markerless_arg:
                marker_responders.append(responder)
        return marker_responders

    @property
    def markerless_responder(self) -> Optional['Responder']:
        """Returns the markerless responder assigned to the component,
        if it exists. If there is no markerless responder configured,
        None is returned.

        A markerless responder is a responder containing an argument
        with its marker set as None. This means it will match against
        any input preceeding the first marker found in the response.

        Returns:
            Responder | None
        """
        for responder in self._responders[self.current_state]:
            if responder.has_markerless_arg:
                return responder
        return None

    def get_primary_markers(self, states: List[Union[str, None]]) -> List['str']:
        """Returns a list of all primary markers for the list of states
        specified."""
        all_markers = []
        for state in states:
            for responder in self._responders[state]:
                for arg in responder.args:
                    if arg.primary:
                        all_markers = all_markers + arg.markers
        return all_markers


class ConsoleAppGuardComponent(ConsoleAppComponent, ABC):
    def __init__(self, app: 'ConsoleApp'):
        super().__init__(app)
        self._show_condition = None

    @property
    def show_condition(self) -> Optional[Callable[[], bool]]:
        return self._show_condition

    @property
    def should_show(self) -> bool:
        return self._show_condition()

    def _configure(self, show_condition: Callable[[], bool]):
        self._show_condition = show_condition

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
        search_and_clear_guard_map(self.app.route_entrance_guard_map)
        search_and_clear_guard_map(self.app.route_exit_guard_map)
