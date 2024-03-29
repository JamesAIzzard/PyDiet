from typing import Any

import model


class BaseQuantityError(model.exceptions.PyDietModelError):
    """Base exception for the quantity module."""

    def __init__(self, subject: Any = None, **kwargs):
        super().__init__(**kwargs)
        self.subject = subject


class UnsupportedExtendedUnitsError(BaseQuantityError):
    """Indicates that bulk properties cannot be set on this object."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class QuantityNotSettableError(BaseQuantityError):
    """Indicates that the quantity cannot be set on this object."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UndefinedQuantityError(BaseQuantityError):
    """Indicates that the quantity associated with this instance has not been set."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class InvalidQtyError(BaseQuantityError, ValueError):
    """The qty is not valid."""

    def __init__(self, quantity: Any, **kwargs):
        super().__init__(**kwargs)
        self.quantity = quantity


class ZeroQtyError(BaseQuantityError, ValueError):
    """Indicates the qty value is zero and cannot be zero."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UndefinedQuantityRatioError(BaseQuantityError):
    """Indicates the quantity ratio is undefined."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SubjectQtyExceedsHostQtyError(BaseQuantityError):
    """Indicates the subject quantity is exceeding the host quantity on a quantity ratio."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ZeroQuantityRatioHostError(ZeroQtyError):
    """Indicates the host quantity is zero, causing a divide-by zero situation."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UnitError(BaseQuantityError):
    """Indicates a general unit error."""

    def __init__(self, unit: Any = None, **kwargs):
        super().__init__(**kwargs)
        self.unit = unit


class IncorrectUnitTypeError(UnitError):
    """A unit of the wrong type has been used."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UnknownUnitError(UnitError):
    """A unit has been used which is not recognised by the system."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UnitNotConfiguredError(UnitError):
    """The data required for this unit is not fully defined."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UndefinedDensityError(UnitNotConfiguredError):
    """The density data is not fully defined."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UndefinedPcMassError(UnitNotConfiguredError):
    """The piece mass data is not fully defined."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

