from pydiet.exceptions import PyDietException


class NameUndefinedError(PyDietException):
    """Indicates the unique name is not defined on the instance."""


class NameDuplicatedError(PyDietException):
    """Indicates the name on the instance is not unique."""


class NoDatafileError(PyDietException):
    """Indicates the datafile was not found."""
