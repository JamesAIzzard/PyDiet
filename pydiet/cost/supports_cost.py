import abc
import copy
from typing import TypedDict, Optional, cast

from pydiet import quantity, cost, PyDietException


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
        

    @property
    def cost_summary(self) -> str:
        if self.cost_fully_defined:
            return '£{cost_per_pref_unit:.2f} per {pref_unit}'.format(
                cost_per_pref_unit=self.cost_per_pref_unit,
                pref_unit=self.pref_units
        else:
            return 'Undefined'

class SupportsCostSetting(SupportsCost):

    def set_cost_per_g(self, cost_per_g: float) -> None:
        cost_per_g = cost.cost_service.validate_cost(cost_per_g)
        self._cost_data['cost_per_g'] = cost_per_g

    def set_cost(self, cost: float, qty: float, unit: str) -> None:
        # Convert the qty into grams;
        qty_g = self.convert_to_g(qty, unit)
        # Set the cost_per_g
        self.set_cost_per_g(qty_g)

    def reset_cost_data(self) -> None:
        self._cost_data['cost_per_g'] = None
        self._cost_data['cost_def_qty'] = None
        self._cost_data['cost_def_unit'] = None
