from model.exceptions import PyDietException


class UniqueValueUndefinedError(PyDietException):
    """Indicates the unique value is not defined on the instance."""


class UniqueValueDuplicatedError(PyDietException):
    """Indicates the unique value on the instance is not unique."""


class DatafileNotFoundError(PyDietException):
    """Indicates the datafile was not found."""


class UniqueValueNotFoundError(PyDietException):
    """Indicates the unique value was not found in the index."""
