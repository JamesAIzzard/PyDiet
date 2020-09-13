from pydiet import PyDietException

class CostDataUndefinedError(PyDietException):
    '''The cost data is undefined.'''
    pass

class CostValueError(PyDietException, ValueError):
    '''The value is not a valid monetary cost.'''
    pass