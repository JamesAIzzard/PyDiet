import abc
from abc import abstractmethod
from typing import Optional, cast

from pydiet import quantity, cost


class SupportsCost(quantity.supports_bulk.SupportsBulk):

    @abc.abstractproperty
    def _cost_per_g(self) -> Optional[float]:
        raise NotImplementedError

    @property
    def cost_per_g(self) -> float:
        if not self.cost_per_g_defined:
            raise cost.exceptions.CostDataUndefinedError
        return cast(float, self._cost_per_g)

    @property
    def cost_per_g_defined(self) -> bool:
        if self._cost_per_g == None:
            return False
        else:
            return True

    @property
    def cost_per_pref_unit(self) -> float:
        return quantity.quantity_service.convert_qty_unit(self.cost_per_g, 'g',
                                                          self.pref_unit, self.readonly_bulk_data['g_per_ml'])

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
        raise NotImplementedError

    def set_cost_per_g(self, cost_per_g: float) -> None:
        cost_per_g = cost.cost_service.validate_cost(cost_per_g)
        self._set_cost_per_g(cost_per_g)

    def set_cost(self, cost: float, qty: float, unit: str) -> None:
        cost_per_unit = cost/qty
        k = quantity.quantity_service.convert_qty_unit(
            1, 'g', unit, 
            self.readonly_bulk_data['g_per_ml'], 
            self.readonly_bulk_data['piece_mass_g'])
        cost_per_g = cost_per_unit*k
        self.set_cost_per_g(cost_per_g)

    def reset_cost_per_g(self) -> None:
        self._set_cost_per_g(None)
