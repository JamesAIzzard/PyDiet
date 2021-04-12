import abc
from typing import Optional

from model import quantity, cost


class SupportsCost(quantity.HasBulk, abc.ABC):
    """ABC for objects supporting abstract cost (costs per qty)."""

    def __init__(self, cost_per_g: Optional[float] = None, **kwargs):
        super().__init__(**kwargs)
        self._cost_per_g: Optional[float] = cost_per_g

    @property
    def cost_per_g(self) -> Optional[float]:
        """Returns the cost of a single gram of the subject."""
        return self._cost_per_g

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

    @property
    def cost_of_ref_qty(self) -> float:
        return self.cost_per_pref_unit * self.ref_qty


class SupportsSettableCost(SupportsCost, abc.ABC):
    """ABC for objects supporting settable abstract cost (costs per qty)."""

    @SupportsCost.cost_per_g.setter
    def cost_per_g(self, cost_per_g: Optional[float]) -> None:
        """Validates and sets cost_per_g"""
        if cost_per_g is None:
            self._cost_per_g = None
        else:
            self._cost_per_g = cost.validation.validate_cost(cost_per_g)

    def set_cost(self, cost_gbp: float, qty: float, unit: str) -> None:
        """Sets the cost in gbp of any quanitity of any unit."""
        # If either of the values are None, just set to None;
        if qty is None or qty == 0:  # To prevent divide by zero.
            self.cost_per_g = None
        else:
            # Find the ratio of cost per original unit
            r = cost_gbp / qty
            # Convert ratio to grams
            k = quantity.convert_qty_unit(
                1, unit, 'g',
                self.g_per_ml,
                self.piece_mass_g)
            cost_per_g = r / k
            self.cost_per_g = cost_per_g
