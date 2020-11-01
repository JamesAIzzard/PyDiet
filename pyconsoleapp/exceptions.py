from typing import Optional


class PyConsoleAppError(Exception):
    """Base exception for PyConsoleApp."""


class PartiallyInitialisedError(PyConsoleAppError):
    """Exception to indicate the requested operation cannot complete because the application is
    partially initialised."""


class NoCurrentRouteError(PyConsoleAppError):
    """Indicating no root route has been configured for the application."""


class InvalidRouteError(PyConsoleAppError):
    """Indicating the requested route is invalid."""


class RouteAlreadyExistsError(PyConsoleAppError):
    """Indicating a route has been added multiple times"""


class NoPrintFunctionError(PyConsoleAppError):
    """Indicating there is no print function available for the component."""


class StateNotFoundError(PyConsoleAppError):
    """Indicating the state which as been set has not been configured on the component."""


class NoCurrentStateError(PyConsoleAppError):
    """Indicating the component has no current state enabled."""


class NoPrimaryArgError(PyConsoleAppError):
    """Indicating responder does not have a primary argument configured."""


class IdenticalPrimaryMarkersError(PyConsoleAppError):
    """Indicating two responders within the same component state have identical primary markers."""


class DuplicateMarkerlessArgError(PyConsoleAppError):
    """Indicating there are multiple markerless arguments assigned to this component state."""


class DuplicateArglessResponderError(PyConsoleAppError):
    """Indicating there are multiple argless responders assigned to this component state."""


class InvalidArgConfigError(PyConsoleAppError):
    """Indicating that the argument configuration is invald."""


class ResponseValidationError(PyConsoleAppError):
    """Indicating the response did not pass validation."""

    def __init__(self, reason: Optional[str] = None, **kwds):
        if reason is None:
            reason = 'The response was invalid.'
        self.reason: Optional[str] = reason


class ArgMissingValueError(ResponseValidationError):
    """Indicating the response is missing an argument value."""

    def __init__(self, arg_name: Optional[str] = None, **kwds):
        if arg_name is None:
            arg_name = "An argument"
        reason = "{arg_name} is missing its value.".format(arg_name=arg_name)
        super().__init__(reason=reason, **kwds)


class OrphanValueError(ResponseValidationError):
    """Indicating there is an unexpected value in the response."""

    def __init__(self, orphan_value: Optional[str] = None, **kwds):
        if orphan_value is not None:
            orphan_value = ": " + orphan_value
        else:
            orphan_value = ''
        super().__init__(reason='There was an unexpected value{orphan_value}.'.format(orphan_value=orphan_value),
                         **kwds)
