from pydiet.exceptions import PyDietException


class CostUndefinedError(PyDietException):
    """Indicating the cost is not defined."""


class CostValueError(PyDietException, ValueError):
    """Indicating the value provided is not a valid cost."""
