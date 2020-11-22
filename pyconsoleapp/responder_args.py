import abc
from typing import List, Callable, Optional, Any

from pyconsoleapp import exceptions


class ResponderArg(abc.ABC):
    """Base class for an argument, representing its markers, validation and default value."""

    def __init__(self, name: str, accepts_value: bool,
                 markers: Optional[List[str]] = None,
                 validators: Optional[List[Callable[..., Any]]] = None,
                 default_value: Any = None,
                 **kwds):

        if accepts_value is False:
            if validators is not None or default_value is not None:  # No validation or defaults on valuless args.
                raise exceptions.InvalidArgConfigError

        self._name: str = name
        self._accepts_value = accepts_value
        self._markers: List[str] = markers if markers is not None else []
        self.marker_found: bool = False
        self._validators: List[Callable[..., Any]] = validators if validators is not None else []
        self._default_value: Optional[Any] = default_value
        self._value: Any = None
        self._value_buffer = []

        self._init_value()

    def _init_value(self) -> None:
        """Initialises/resets the argument value"""
        # If we accept a value and have a default, set the value as default (using validators in setter).
        if self.accepts_value is True and self._default_value is not None:
            self.value = self._default_value
        # If we don't accept a value;
        elif self.accepts_value is False:
            # Valuless values start at False;
            self.value = False

    @property
    def name(self) -> str:
        """Returns the argument's name."""
        return self._name

    @property
    def is_primary(self) -> bool:
        """Returns True/False to indicate if the argument is primary."""
        return isinstance(self, PrimaryArg)

    @property
    def value(self) -> Any:
        """Returns the argument's value."""
        return self._value

    @value.setter
    def value(self, value: Any) -> None:
        """Sets the argument's value, via any registered validators."""
        # First check we aren't trying to set an arbitrary value on a valueless arg;
        if not self.accepts_value and not isinstance(value, bool):
            raise ValueError('Valueless args should only be given boolean values.')
        # Now use the validators to set the value;
        temp_value = value
        for validator in self._validators:
            temp_value = validator(temp_value)
        self._value = temp_value

    def buffer_value(self, value_fragment: Any) -> None:
        """Adds the value fragment to the value buffer."""
        # Raise exception if we try and buffer a valueless arg;
        if not self._accepts_value:
            raise exceptions.OrphanValueError(value_fragment)

        self._value_buffer.append(value_fragment)

    def write_value_buffer(self) -> None:
        """Concatenates the value buffer and submits it for validation via the value setter."""
        # If don't accept values;
        if not self._accepts_value:
            # Check the buffer is empty and write true, otherwise shout;
            if len(self._value_buffer) == 0:
                self.value = True
            else:
                raise exceptions.OrphanValueError(' '.join(self._value_buffer))
        # If we do accept values;
        elif self._accepts_value:
            # If the buffer is empty;
            if len(self._value_buffer) == 0:
                # Shout if the marker has been found but buffer is empty (never OK for an valued arg);
                if self.marker_found:
                    raise exceptions.ArgMissingValueError('{arg_name}'.format(arg_name=self.name.replace('_', ' ')))
                # Shout if markerless primary and no default;
                if self.is_markerless and self.is_primary and self._default_value is None:
                    raise exceptions.ArgMissingValueError('{arg_name}'.format(arg_name=self.name.replace('_', ' ')))
            # Buffer is not empty;
            else:
                self.value = ' '.join(self._value_buffer)
        # Whatever happened, clear the buffer;
        self._value_buffer = []

    @property
    def accepts_value(self) -> bool:
        """Returns True/False to indicate if the argument can be given a value."""
        return self._accepts_value

    @property
    def markers(self) -> List[str]:
        """Returns a list of the argument's markers."""
        return self._markers

    @property
    def is_markerless(self) -> bool:
        """Returns True/False to indicate if this arg has any markers."""
        if len(self._markers):
            return False
        else:
            return True

    def reset(self) -> None:
        """Resets the arg value."""
        self.marker_found = False
        self._init_value()


class PrimaryArg(ResponderArg):
    """Represents a mandatory Responder argument."""

    def __init__(self, **kwds):
        super().__init__(**kwds)


class OptionalArg(ResponderArg):
    """Represents an optional Responder argument."""

    def __init__(self, **kwds):
        super().__init__(**kwds)
