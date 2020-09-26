from pydiet import PyDietException


class UnitError(PyDietException):
    """Indicates a general unit error."""


class IncorrectUnitTypeError(UnitError):
    """A unit of the wrong type has been used."""


class UnknownUnitError(UnitError):
    """A unit has been used which is not recognised by the system."""


class UnitNotConfiguredError(UnitError):
    """The data required for this unit is not fully defined."""


class DensityNotConfiguredError(UnitNotConfiguredError):
    """The density data is not fully defined."""


class PcMassNotConfiguredError(UnitNotConfiguredError):
    """The piece mass data is not fully defined."""


class InvalidQtyError(PyDietException):
    """The value is not a valid qty."""
