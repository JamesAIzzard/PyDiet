from inspect import signature
from typing import Callable, List, Dict, Any, Optional, TYPE_CHECKING

from pyconsoleapp import exceptions

if TYPE_CHECKING:
    from pyconsoleapp import ConsoleApp
    from pyconsoleapp.responder_args import ResponderArg


class Responder:
    """Associates a function with a list of arguments."""

    def __init__(self, app: 'ConsoleApp', func: Callable[..., None], args: Optional[List['ResponderArg']] = None,
                 **kwds):
        self._app: 'ConsoleApp' = app
        self._responder_func: Callable[..., None] = func
        self._args: List['ResponderArg'] = args if args is not None else []

        self._markerless_arg: Optional['ResponderArg'] = None
        for arg in self._args:
            if arg.is_markerless:
                if self._markerless_arg is None:
                    self._markerless_arg = arg
                else:
                    raise exceptions.DuplicateMarkerlessArgError

        super().__init__(**kwds)

    @property
    def has_markerless_arg(self) -> bool:
        """Returns True/False to indicate if any constituent args are markerless."""
        return self._markerless_arg is not None

    @property
    def markerless_arg(self) -> Optional['ResponderArg']:
        """Returns the responder's markerless arg, if exists, otherwise returns None."""
        return self._markerless_arg

    @property
    def has_marker_args(self) -> bool:
        """Returns True/False to indicate if any constituent args have markers."""
        if self.has_markerless_arg:
            return len(self._args) > 1
        else:
            return len(self._args) > 0

    @property
    def _all_markers(self) -> List[str]:
        """Returns a list of all markers associated with all args on this responder."""
        markers = []
        for arg in self._args:
            markers.extend(arg.markers)
        return markers

    @property
    def is_argless(self) -> bool:
        """Returns True/False to indicate if the responder is argless."""
        return len(self._args) == 0

    @property
    def _primary_args(self) -> List['ResponderArg']:
        """Returns a list of the primary arguments assigned to this responder."""
        primary_args = []
        for arg in self._args:
            if arg.is_primary:
                primary_args.append(arg)
        return primary_args

    @property
    def _args_and_values(self) -> Dict[str, Any]:
        """Returns a dictionary of all arg names and their current values."""
        kwds = {}
        for arg in self._args:
            kwds[arg.name] = arg.value
        return kwds

    def _reset_args(self) -> None:
        """Resets the associated ResponderArg values."""
        for arg in self._args:
            arg.reset()

    def check_marker_match(self, response: str) -> bool:
        """Returns True/False to indicate if the given response matches this responder."""
        split_response = set(response.split())
        for arg in self._primary_args:
            if len(split_response.intersection(set(arg.markers))) == 0:
                return False
        return True

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Distributes the values in the response to their respective arguments.
        Notes:
        - Any present valueless arguments are set to True.
        - All argument validation occurs in the argument setters."""

        def word_is_marker(word: str) -> bool:
            """Returns True/False to indicate if word is a marker for an arg on this responder."""
            return word in self._all_markers

        def get_arg_for_marker(marker: str) -> 'ResponderArg':
            """Returns the ResponderArg corresponding to the marker specified."""
            for arg in self._args:
                if marker in arg.markers:
                    return arg
            raise ValueError('{marker} is not a marker for any args.'.format(marker=marker))

        words = response.split()  # Split the response into a list of words.
        current_arg = self.markerless_arg  # None if no markerless arg exists.

        # Cycle through each word in the response;
        for current_word in words:
            # Is the word a marker or part of a value?
            # If it is a marker, write the buffer on the previous arg and update the current arg;
            if word_is_marker(current_word):
                if current_arg is not None:
                    current_arg.write_value_buffer()
                current_arg = get_arg_for_marker(current_word)
                current_arg.marker_found = True
            # If it is a value, just add it to the buffer;
            else:
                current_arg.buffer_value(current_word)
        # We have run out of words, so write any residual buffer;
        current_arg.write_value_buffer()

        # Return the kwds dict;
        return self._args_and_values

    def respond(self, response: Optional[str] = None) -> None:
        """Calls the function associated with the responder, passing any parsed arguments, if present."""
        self._app.stop_responding()  # Stop by default, and the function can then restart before next loop.
        if self.is_argless:
            self._responder_func()
        else:
            func_sig = signature(self._responder_func)
            if len(func_sig.parameters) > 0:
                kwds = self._parse_response(response)
                self._responder_func(**kwds)
            else:
                self._responder_func()
            self._reset_args()
