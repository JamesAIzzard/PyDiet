import abc
from typing import Optional

from model import quantity, cost


class SupportsCost(quantity.HasBulk, abc.ABC):
    """ABC for objects supporting abstract cost (costs per qty)."""

    def __init__(self, cost_per_g: Optional[float] = None, **kwargs):
        self._cost_per_g: Optional[float] = cost_per_g
        super().__init__(**kwargs)

    def _set_cost_per_g(self, cost_per_g: Optional[float]):
        """Customisable implementation for setting the cost_per_g field."""
        raise cost.exceptions.CostNotSettableError

    @property
    def cost_per_g(self) -> Optional[float]:
        """Return's the subject's cost per gram."""
        return self._cost_per_g

    @cost_per_g.setter
    def cost_per_g(self, cost_per_g: Optional[float]):
        """Set's the object's cost per gram."""
        self._set_cost_per_g(cost_per_g)

    @property
    def cost_per_g_defined(self) -> bool:
        """Returns True/False to indicate if the object's cost per gram is defined."""
        return self.cost_per_g is not None

    @property
    def cost_per_pref_unit(self) -> float:
        """Returns the cost of one of the instance's preferred units."""
        if not self.cost_per_g_defined:
            raise cost.exceptions.CostUndefinedError
        return quantity.convert_qty_unit(qty=self.cost_per_g,
                                         start_unit='g',
                                         end_unit=self.pref_unit,
                                         g_per_ml=self.g_per_ml,
                                         piece_mass_g=self.piece_mass_g)


class SupportsSettableCost(SupportsCost, abc.ABC):
    """ABC for objects supporting settable abstract cost (costs per qty)."""

    def _set_cost_per_g(self, cost_per_g: Optional[float]) -> None:
        """Validates and sets cost_per_g"""
        if cost_per_g is None:
            self._set_cost_per_g(None)
        else:
            self._set_cost_per_g(cost.validation.validate_cost(cost_per_g))

    def set_cost(self, cost_gbp: float, qty: float, unit: str) -> None:
        """Sets the cost in gbp of any quanitity of any unit."""
        # Todo - Need to finish updating HasBulk to use its properties here.
        cost_per_unit = cost_gbp / qty
        k = quantity.convert_qty_unit(
            1, 'g', unit,
            self._bulk_data['g_per_ml'],
            self._bulk_data['piece_mass_g'])
        cost_per_g = cost_per_unit * k
        self.set_cost_per_g(cost_per_g)
