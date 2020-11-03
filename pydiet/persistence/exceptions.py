from pydiet.exceptions import PyDietException


class NameUndefinedError(PyDietException):
    pass


class NameDuplicatedError(PyDietException):
    pass


class NoDatafileError(PyDietException):
    pass
