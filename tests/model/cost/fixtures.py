from typing import Callable, Optional

import model


class SupportsCostPerQuantityTestable(model.cost.SupportsCostPerQuantity):
    def __init__(self,
                 pref_unit: str = 'g',
                 ref_qty: float = 100,
                 cost_per_g: Optional[float] = None):
        super().__init__()
        self._cost_data_ = model.cost.CostPerQtyData(
            pref_unit=pref_unit,
            ref_qty=ref_qty,
            cost_per_g=cost_per_g
        )

    @property
    def _cost_per_qty_data(self) -> 'model.cost.CostPerQtyData':
        return self._cost_data_
