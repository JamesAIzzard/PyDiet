"""Fixtures for testing quantity module.
"""
from typing import Callable, Optional

import model


class SupportsExtendedUnitsTestable(model.quantity.SupportsExtendedUnits):
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


def get_qty_data_src(
        qty_in_g: Optional[float] = None,
        pref_unit: str = 'g'
) -> Callable[[None], 'model.quantity.QuantityData']:
    """Creates and returns a Callable which returns quantity data when called.
    Provides default values, unless values are specified.
    """
    return lambda: model.quantity.QuantityData(
        quantity_in_g=qty_in_g,
        pref_unit=pref_unit
    )


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
