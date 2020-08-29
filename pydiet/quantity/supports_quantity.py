import abc
from typing import TypedDict, Optional, Protocol

from pydiet import quantity


class QuantityData(TypedDict):
    qty_g: Optional[float]
    pref_qty_units: Optional[str]


quantity_data_template = {
    'qty': None,
    'pref_qty_units': None
}


class SupportsQuantity(quantity.supports_density.SupportsDensity,
                       Protocol):

    @abc.abstractproperty
    def readonly_quantity_data(self) -> QuantityData:
        raise NotImplementedError

    @property
    def quantity_g(self) -> float:
        if not self.quantity_is_defined:
            raise quantity.exceptions.QuantityUndefinedError
        return self.readonly_quantity_data['qty']

    @property
    def quantity_units(self) -> str:
        if not self.quantity_is_defined:
            raise quantity.exceptions.QuantityUndefinedError
        return self.readonly_quantity_data['qty_units']

    @property
    def quantity_is_defined(self) -> bool:
        for value in self.readonly_quantity_data.values():
            if value == None:
                return False
        return True
