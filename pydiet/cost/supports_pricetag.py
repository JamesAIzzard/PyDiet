from pydiet.quantity.supports_quantity import SupportsQuantity
from pydiet import cost, quantity


class SupportsPricetag(cost.supports_cost.SupportsCost,
                       quantity.supports_quantity.SupportsQuantity):

    @property
    def pricetag(self) -> float:
        return self.cost_per_g*self.quantity_g
