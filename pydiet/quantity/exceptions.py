from pydiet import PyDietException

class UnknownUnitError(PyDietException):
    '''A unit has been used which is not recognised by the system.'''
    pass

class UnitNotConfiguredError(PyDietException):
    '''The data required for this unit is not fully defined.'''
    pass

class DensityNotConfiguredError(PyDietException):
    '''The density data is not fully defined.'''
    pass

class PcMassNotConfiguredError(PyDietException):
    '''The piece mass data is not fully defined.'''
    pass

class InvalidQtyError(PyDietException):
    '''The value is not a valid qty.'''
    pass