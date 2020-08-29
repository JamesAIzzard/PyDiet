import abc
from typing import TypedDict, Optional, Protocol

from pydiet import quantity, cost


class CostData(TypedDict):
    cost_per_g: Optional[float]
    pref_cost_qty_units: Optional[str]


cost_data_template: 'CostData' = {
    "cost_per_g": None,
    "pref_cost_qty_units": None
}


class SupportsCost(
    quantity.supports_density.SupportsDensity,
    quantity.supports_unit_mass.SupportsUnitMass,
    Protocol):

    @abc.abstractproperty
    def readonly_cost_data(self) -> 'CostData':
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
        return self.readonly_cost_data['pref_qty_units']

    @property
    def cost_is_defined(self) -> bool:
        for value in self.readonly_cost_data.values():
            if value == None:
                return False
        return True


class SupportsCostSetting(SupportsCost, Protocol):

    @abc.abstractproperty
    def cost_data(self) -> 'CostData':
        raise NotImplementedError

    def set_cost_per_g(self, cost_per_g: float, pref_cost_qty_units: str) -> None:
        # Validate things;
        pref_cost_qty_units = quantity.quantity_service.validate_qty_unit(
            pref_cost_qty_units)
        cost_per_g = float(cost_per_g)
        # Set the data;
        self.cost_data['cost_per_g'] = cost_per_g
        self.cost_data['pref_qty_units'] = pref_cost_qty_units

    def set_cost_any_units(self, cost:float, cost_qty:float, cost_qty_units:str) -> None:
        # £12.00 per 1kg of tomato
        # Convert the cost_qty into g;
        qty_g = quantity.quantity_service.convert_qty_to_g(cost_qty, cost_qty_units, g_per_ml=self.g_per_ml)