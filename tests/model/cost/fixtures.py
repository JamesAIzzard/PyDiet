from typing import Callable, Optional

import model


class SupportsCostTestable(model.cost.SupportsCost):
    def __init__(self,
                 pref_unit: str = 'g',
                 ref_qty: float = 100,
                 cost_per_g: Optional[float] = None):
        super().__init__()
        self._cost_data_ = model.cost.CostData(
            pref_unit=pref_unit,
            ref_qty=ref_qty,
            cost_per_g=cost_per_g
        )

    @property
    def _cost_data(self) -> 'model.cost.CostData':
        return self._cost_data_
