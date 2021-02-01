from model.exceptions import PyDietException


class BulkNotSettableError(PyDietException):
    """Indicates that the bulk cannot be set on this object."""


class QuantityNotSettableError(PyDietException):
    """Indicates that the quantity cannot be set on this object."""


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
    """The qty is not a valid qty."""
