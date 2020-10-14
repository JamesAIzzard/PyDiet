import abc, copy
from typing import TypedDict, Optional, cast

from pydiet import quantity


class QuantityData(TypedDict):
    qty_g: Optional[float]
    pref_qty_units: Optional[str]


quantity_data_template:'QuantityData' = {
    'qty_g': None,
    'pref_qty_units': None
}


class SupportsQuantity(quantity.supports_bulk.SupportsBulk):
    @property
    @abc.abstractmethod
    def _quantity_data(self) -> 'QuantityData':
        raise NotImplementedError

    @property
    def quantity_data(self) -> 'QuantityData':
        return copy.deepcopy(self._quantity_data)

    @property
    def quantity_g(self) -> Optional[float]:
        return self.quantity_data['qty_g']

    @property
    def pref_quantity_units(self) -> str:
        return self.quantity_data['pref_qty_units']

    @property
    def quantity_is_defined(self) -> bool:
        for value in self.quantity_data.values():
            if value == None:
                return False
        return True

class SupportsQuantitySetting(SupportsQuantity):
    
    def set_quantity_g(self, qty_g:float, pref_qty_units:str) -> None:
        raise NotImplementedError
