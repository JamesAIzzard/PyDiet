from pydiet.exceptions import PyDietException


class NameNotSettableError(PyDietException):
    """Indicating that the name cannot be set on this object.
    Note:
        Inherit from HasSettableName for a settable name.
    """
