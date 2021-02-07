from model import cost, quantity


class SupportsPricetag(cost.SupportsCost, quantity.SupportsQuantity):

    @property
    def pricetag(self) -> float:
        return self.cost_per_g*self.quantity_g
