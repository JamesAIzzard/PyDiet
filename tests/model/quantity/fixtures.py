from typing import Optional

import model


class HasQuantityTester(model.quantity.HasQuantity):
    """Minimal implementation of HasQuantity for testing purposes."""

    def __init__(self):
        super().__init__(subject=model.quantity.HasBulk())
        self._quantity_in_g: Optional[float] = None
        self._quantity_pref_unit: str = 'g'

    def _get_quantity_in_g(self) -> Optional[float]:
        return self._quantity_in_g

    def _get_quantity_pref_unit(self) -> str:
        return self._quantity_pref_unit


def get_has_bulk_with_09_density() -> 'model.quantity.HasBulk':
    return model.quantity.HasBulk(model.quantity.BulkData(
        ref_qty=100,
        pref_unit='g',
        g_per_ml=0.9,
        piece_mass_g=None
    ))


def get_has_bulk_with_30_pc_mass() -> 'model.quantity.HasBulk':
    return model.quantity.HasBulk(model.quantity.BulkData(
        ref_qty=100,
        pref_unit='g',
        g_per_ml=None,
        piece_mass_g=30
    ))


def get_undefined_has_quantity() -> 'model.quantity.HasQuantity':
    return HasQuantityTester()


def get_has_3kg() -> 'model.quantity.HasQuantity':
    hq = HasQuantityTester()
    hq._quantity_in_g = 3000
    hq._quantity_pref_unit = 'kg'
    return hq


def get_undefined_has_settable_quantity() -> 'model.quantity.HasSettableQuantity':
    return model.quantity.HasSettableQuantity(subject=model.quantity.HasBulk())
