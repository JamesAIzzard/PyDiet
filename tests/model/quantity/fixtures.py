from unittest import mock
from typing import Callable, Optional

import model


class SupportsExtendedUnitsTestable(model.quantity.SupportsExtendedUnits):
    def __init__(self, g_per_ml: float = None, peice_mass_g: float = None, **kwargs):
        super().__init__(**kwargs)
        self._g_per_ml_ = g_per_ml
        self._piece_mass_g_ = peice_mass_g

    @property
    def _g_per_ml(self) -> Optional[float]:
        return self._g_per_ml_

    @property
    def _piece_mass_g(self) -> Optional[float]:
        return self._piece_mass_g_


def get_qty_data_src(qty_in_g: Optional[float] = None, pref_unit: str = 'g') -> Callable[
    [None], 'model.quantity.QuantityData']:
    return lambda: model.quantity.QuantityData(
        quantity_in_g=qty_in_g,
        pref_unit=pref_unit
    )


def get_subject_without_extended_units() -> 'mock.Mock':
    return mock.Mock()


def get_subject_with_density(g_per_ml: Optional[float] = None) -> 'SupportsExtendedUnitsTestable':
    return SupportsExtendedUnitsTestable(g_per_ml=g_per_ml)


def get_subject_with_pc_mass(peice_mass_g: Optional[float] = None) -> 'SupportsExtendedUnitsTestable':
    return SupportsExtendedUnitsTestable(peice_mass_g=peice_mass_g)
