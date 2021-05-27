"""Test fixtures to help with testing the cost module."""
from typing import Optional

import model


class SupportsCostPerQuantityTestable(model.cost.SupportsCostPerQuantity):
    """Minimal concrete implementation for use with testing the SupportsCostPerQuantity
    base class."""

    def __init__(self,
                 pref_unit: str = 'g',
                 ref_qty_g: Optional[float] = 100,
                 cost_per_g: Optional[float] = None):
        super().__init__()
        self.pref_unit = pref_unit
        self.ref_qty_g = ref_qty_g
        self._cost_per_g_ = cost_per_g

    @property
    def _cost_per_qty_data(self) -> 'model.cost.CostPerQtyData':
        return model.cost.CostPerQtyData(
            quantity_in_g=self.ref_qty_g,
            pref_unit=self.pref_unit,
            cost_per_g=self._cost_per_g_
        )


def get_cost_per_qty_data(quantity_in_g: Optional[float] = None, pref_unit: str = 'g') -> 'model.cost.CostPerQtyData':
    """Returns CostPerQtyData instance, with defaults if values not specified."""
    return model.cost.CostPerQtyData(
        quantity_in_g=quantity_in_g,
        pref_unit=pref_unit
    )
