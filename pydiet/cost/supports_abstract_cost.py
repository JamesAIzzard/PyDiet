import abc
from typing import Dict, Union, Optional, cast

from pydiet import quantity, cost

abstract_cost_data_template = {
    "cost_per_g": None,
    "mass_g": None,
    "pref_qty_units": None
}

class SupportsAbstractCost(quantity.supports_density.SupportsDensity):

    @abc.abstractproperty
    def readonly_cost_data(self) ->Dict[str, Union[str, float]]:
        raise NotImplementedError   

    @property
    def cost_per_g(self) -> float:
        if not self.cost_is_defined:
            raise cost.exceptions.CostDataUndefinedError
        return self.readonly_cost_data['cost_per_g']/self.readonly_cost_data['mass_g']

    @property
    def pref_cost_qty_units(self) -> str:
        if not self.cost_is_defined:
            raise cost.exceptions.CostDataUndefinedError
        return cast(str, self.readonly_cost_data['pref_qty_units'])

    @property
    def cost_is_defined(self) -> bool:
        for value in self.readonly_cost_data.values():
            if value == None:
                return False
        return True