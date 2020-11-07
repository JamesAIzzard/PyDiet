from pydiet.exceptions import PyDietException


class CostNotSettableError(PyDietException):
    """Indicating the object does not allow cost setting."""


class CostUndefinedError(PyDietException):
    """Indicating the cost is not defined."""


class CostValueError(PyDietException, ValueError):
    """Indicating the qty provided is not a valid cost."""
