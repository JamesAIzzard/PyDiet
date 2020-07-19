import pydiet

class DatafileNameUndefinedError(pydiet.exceptions.PyDietException):
    pass

class DuplicateDatafileNameError(pydiet.exceptions.PyDietException):
    pass

class NameNotFoundError(pydiet.exceptions.PyDietException):
    pass