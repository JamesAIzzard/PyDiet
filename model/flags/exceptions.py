from pydiet.exceptions import PyDietException


class FlagNameError(PyDietException):
    """The flag name is not recognised."""


class FlagValueError(PyDietException):
    """The flag qty is not True, False or None."""
