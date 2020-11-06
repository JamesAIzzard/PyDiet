import abc
from typing import Optional

from pydiet import quantity, cost
from pydiet.cost import validation, exceptions


class SupportsCost(quantity.HasBulk, abc.ABC):
    """ABC for objects supporting abstract cost (costs per qty)."""

    def __init__(self, cost_per_g: Optional[float] = None, **kwds):
        self._cost_per_g: Optional[float] = cost_per_g
        super().__init__(**kwds)

    @property
    def cost_per_g(self) -> Optional[float]:
        """Return's the subject's cost per gram."""
        return self._cost_per_g

    # Todo - Link to private function which we can manipulate to enforce readonly/writable behaviour.
    @cost_per_g.setter
    def cost_per_g(self, cost_per_g: Optional[float]):
        """Set's the object's cost per gram."""
        if cost_per_g is None:
            self._cost_per_g = None
        else:
            self._cost_per_g = validation.validate_cost(cost_per_g)

    @property
    def cost_per_g_defined(self) -> bool:
        """Returns True/False to indicate if the object's cost per gram is defined."""
        return self.cost_per_g is not None

    @property
    def cost_per_pref_unit(self) -> float:
        """Returns the cost of one of the instance's preferred units."""
        if not self.cost_per_g_defined:
            raise exceptions.CostUndefinedError
        return quantity.convert_qty_unit(qty=self.cost_per_g,
                                         start_unit='g',
                                         end_unit=self.pref_unit,
                                         g_per_ml=self.g_per_ml,
                                         piece_mass_g=self.piece_mass_g)

    @property
    def cost_summary(self) -> str:
        """Returns a readable summary of the object's cost data."""
        if self.cost_per_g_defined:
            cost_per_ref_qty = self.ref_qty_in_g * self.cost_per_g
            return '£{cost:.2f} per {ref_qty}{ref_unit}'.format(
                cost=cost_per_ref_qty,
                ref_qty=self.ref_qty,
                ref_unit=self.ref_unit
            )
        else:
            return 'Undefined'


class SupportsSettableCost(SupportsCost):
    """ABC for objects supporting settable abstract cost (costs per qty)."""

    @abstractmethod
    def _set_cost_per_g(self, validated_cost_per_g: Optional[float]) -> None:
        """Writes a validated cost_per_g to the correct field."""
        raise NotImplementedError

    def set_cost_per_g(self, cost_per_g: Optional[float]) -> None:
        """Validates cost per gram before writing it."""
        if cost_per_g is not None:
            cost_per_g = cost.cost_service.validate_cost(cost_per_g)
        self._set_cost_per_g(cost_per_g)

    def set_cost(self, cost_gbp: float, qty: float, unit: str) -> None:
        """Sets the cost in gbp of any quanitity of any unit."""
        cost_per_unit = cost_gbp / qty
        k = quantity.core.convert_qty_unit(
            1, 'g', unit,
            self._bulk_data['g_per_ml'],
            self._bulk_data['piece_mass_g'])
        cost_per_g = cost_per_unit * k
        self.set_cost_per_g(cost_per_g)

    def reset_cost(self) -> None:
        self.set_cost_per_g(None)
