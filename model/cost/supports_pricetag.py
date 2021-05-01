import abc

from . import SupportsCost
import model


class HasPricetagOf(SupportsCost, model.quantity.HasQuantityOf, abc.ABC):
    """Returns the prince of the amount of the instance."""

    @property
    def pricetag(self) -> float:
        return self.cost_per_g * self.quantity_in_g
