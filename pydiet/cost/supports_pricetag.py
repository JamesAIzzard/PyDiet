from pydiet import quantity

from pydiet import cost


class SupportsExactCost(cost.supports_general_cost.SupportsGeneralCost,
                        quantity.supports_quantity.SupportsQuantity):
    @property
    def cost(self) -> float:
        return self.cost_per_g*self.quantity_g
