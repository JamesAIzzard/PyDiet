import abc
import copy
from typing import TypedDict, Optional, cast

from pydiet import quantity, cost


class CostData(TypedDict):
    cost_per_g: Optional[float]
    pref_cost_qty_units: Optional[str]


def get_empty_cost_data() -> 'CostData':
    return CostData(cost_per_g=None,
                    pref_cost_qty_units=None)


class SupportsCost(quantity.supports_bulk.SupportsBulk):

    @abc.abstractproperty
    def _cost_data(self) -> 'CostData':
        raise NotImplementedError

    @property
    def readonly_cost_data(self) -> 'CostData':
        return copy.deepcopy(self._cost_data)

    @property
    def cost_summary(self) -> str:
        return 'A cost summary.'

    @property
    def cost_per_g(self) -> float:
        if not self.cost_is_defined:
            raise cost.exceptions.CostDataUndefinedError
        return cast(float, self.readonly_cost_data['cost_per_g'])

    @property
    def pref_cost_qty_units(self) -> str:
        if not self.cost_is_defined:
            raise cost.exceptions.CostDataUndefinedError
        return cast(str, self.readonly_cost_data['pref_cost_qty_units'])

    @property
    def cost_is_defined(self) -> bool:
        for value in self.readonly_cost_data.values():
            if value == None:
                return False
        return True


class SupportsCostSetting(SupportsCost):

    def set_cost_per_g(self, cost_per_g: float, pref_cost_qty_units: str) -> None:
        # Validate things;
        pref_cost_qty_units = quantity.quantity_service.validate_qty_unit(
            pref_cost_qty_units)
        cost_per_g = float(cost_per_g)
        # Set the data;
        self._cost_data['cost_per_g'] = cost_per_g
        self._cost_data['pref_cost_qty_units'] = pref_cost_qty_units

    def set_cost_any_units(self, cost: float, cost_qty: float, cost_qty_units: str) -> None:
        raise NotImplementedError
