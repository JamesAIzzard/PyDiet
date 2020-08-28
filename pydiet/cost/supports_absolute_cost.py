from pydiet import quantity
from typing import cast

from pydiet import cost


class SupportsAbsoluteCost(cost.supports_abstract_cost.SupportsAbstractCost,
                           quantity.supports_quantity.SupportsQuantity):
    @property
    def cost(self) -> float:
        return self.cost_per_g
