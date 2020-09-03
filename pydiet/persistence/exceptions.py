import pydiet

class UniqueFieldUndefinedError(pydiet.exceptions.PyDietException):
    pass

class UniqueValueDuplicatedError(pydiet.exceptions.PyDietException):
    pass

class NoDatafileError(pydiet.exceptions.PyDietException):
    pass