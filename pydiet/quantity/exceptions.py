from pydiet.exceptions import PyDietException
import pydiet

class UnknownUnitError(pydiet.exceptions.PyDietException):
    pass

class DensityDataUndefinedError(pydiet.exceptions.PyDietException):
    pass

class PcMassDataUndefinedError(pydiet.exceptions.PyDietException):
    pass

class QuantityUndefinedError(pydiet.exceptions.PyDietException):
    pass