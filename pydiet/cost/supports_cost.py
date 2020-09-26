import abc
from abc import abstractmethod
from typing import Optional

from pydiet import quantity, cost


class SupportsCost(quantity.supports_bulk.SupportsBulk, abc.ABC):

    @property
    @abc.abstractmethod
    def cost_per_g(self) -> Optional[float]:
        raise NotImplementedError

    @property
    def cost_per_g_defined(self) -> bool:
        if self.cost_per_g is None:
            return False
        else:
            return True

    @property
    def cost_per_pref_unit(self) -> float:
        """Returns the cost of one of the instance's preferred units."""
        return quantity.quantity_service.convert_qty_unit(self.cost_per_g, 'g',
                                                          self.pref_unit, self._bulk_data['g_per_ml'])

    @property
    def cost_summary(self) -> str:
        if self.cost_per_g_defined:
            return '£{cost_per_pref_unit:.4f} per {pref_unit}'.format(
                cost_per_pref_unit=self.cost_per_pref_unit,
                pref_unit=self.pref_unit)
        else:
            return 'Undefined'


class SupportsCostSetting(SupportsCost):

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
        k = quantity.quantity_service.convert_qty_unit(
            1, 'g', unit,
            self._bulk_data['g_per_ml'],
            self._bulk_data['piece_mass_g'])
        cost_per_g = cost_per_unit * k
        self.set_cost_per_g(cost_per_g)

    def reset_cost(self) -> None:
        self.set_cost_per_g(None)
