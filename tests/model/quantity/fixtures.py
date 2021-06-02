"""Fixtures for testing quantity module."""
from typing import Callable, Optional, Any

import model


class HasReadableQuantityOfTestable(model.quantity.HasReadableQuantityOf):
    """Minimal implementation of BaseQuantityOf for testing."""

    def __init__(self, qty_subject: Any, quantity_data: 'model.quantity.QuantityData'):
        super().__init__(qty_subject=qty_subject)

        self._quantity_data = quantity_data

    @property
    def _quantity_in_g(self) -> Optional[float]:
        """Returns the raw quantity in g from the local storage."""
        return self._quantity_data['quantity_in_g']

    @property
    def _unvalidated_pref_unit(self) -> str:
        """Returns the raw pref unit from the local storage."""
        return self._quantity_data['pref_unit']


class HasReadableExtendedUnitsTestable(model.quantity.HasReadableExtendedUnits):
    """Minimal concrete implementation of the SupportsExtendedUnits base class."""

    def __init__(self, g_per_ml: float = None, piece_mass_g: float = None, **kwargs):
        super().__init__(**kwargs)
        self._g_per_ml_ = g_per_ml
        self._piece_mass_g_ = piece_mass_g

    @property
    def _g_per_ml(self) -> Optional[float]:
        return self._g_per_ml_

    @property
    def _piece_mass_g(self) -> Optional[float]:
        return self._piece_mass_g_


class IsRatioBaseTestable(model.quantity.HasRatioOf):
    """Minimal implementation to allow testing of IsRatioBase class."""

    def __init__(self,
                 numerator: Any,
                 denominator: Any,
    ):
        """Constructor
        Notes:
            I opted to pass in numerator and denominator instances, instead of just their
            data, because that allowed me to configure them with things like extended units.
            This allows testing ratio functionality that relies on the denominator/numerator
            having particular attributes.
        """
        self._numerator = numerator
        self._denominator = denominator

    @property
    def numerator(self) -> Any:
        """Returns the numerator."""
        return self._numerator

    @property
    def denominator(self) -> Any:
        """Returns the denominator."""
        return self._denominator


def get_qty_data(
        qty_in_g: Optional[float] = None,
        pref_unit: str = 'g'
) -> 'model.quantity.QuantityData':
    """Creates and returns a quantity data instance, with default values for any
    non specified values."""
    return model.quantity.QuantityData(
        quantity_in_g=qty_in_g,
        pref_unit=pref_unit
    )


def get_qty_data_src(quantity_data: 'model.quantity.QuantityData') -> Callable[[None], 'model.quantity.QuantityData']:
    """Creates and returns a Callable which returns quantity data when called.
    Provides default values, unless values are specified.
    """
    return lambda: quantity_data


def get_extended_units_data(g_per_ml: Optional[float] = None, piece_mass_g: Optional[float] = None):
    """Configures and returns an extended units data instance. Essentially, this
    just provides some defaults for the data class.
    - If density is defined, g_per_ml is set to 1.2
    - If pc mass is defined, piece_mass_g is set to 150.
    """
    return model.quantity.ExtendedUnitsData(
        g_per_ml=g_per_ml if g_per_ml is not None else None,
        piece_mass_g=piece_mass_g if piece_mass_g is not None else None
    )
