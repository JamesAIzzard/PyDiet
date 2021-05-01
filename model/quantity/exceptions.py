from typing import Any, Union, Optional

import model


class BaseQuantityError(model.exceptions.PyDietModelError):
    """Base exception for the quantity module."""

    def __init__(self, subject: Optional[Union[
        'model.quantity.HasBulk',
        'model.quantity.HasSettableBulk',
        'model.quantity.HasQuantity',
        'model.quantity.HasSettableQuantity'
    ]] = None, **kwargs):
        super().__init__(**kwargs)
        self.subject = subject


class BulkNotSettableError(BaseQuantityError):
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


class DensityInUseError(BaseQuantityError):
    """Indicating the action cannot occur because the density is in use."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UndefinedPcMassError(UnitNotConfiguredError):
    """The piece mass data is not fully defined."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class PcMassInUseError(BaseQuantityError):
    """Indicating the action cannot occur because the peice mass is in use."""

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
