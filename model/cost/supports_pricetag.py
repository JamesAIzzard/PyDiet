from model import cost, quantity


class HasPricetag(cost.SupportsCost, quantity.HasQuantity):

    @property
    def pricetag(self) -> float:
        return self.cost_per_g*self.quantity_g
