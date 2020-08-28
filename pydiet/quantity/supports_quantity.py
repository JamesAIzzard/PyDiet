import abc
from typing import Dict, Union, cast

quantity_data_template = {
    'qty' : None,
    'qty_units' : None
}

# TODO - I think I should be using TypedDict here.

class SupportsQuantity(abc.ABC):

    @abc.abstractproperty
    def readonly_quantity_data(self) -> Dict[str, Union[float, str]]:
        raise NotImplementedError  

    @abc.abstractproperty
    def quantity(self)->float:
        if not self.quantity_is_defined:
            raise quantity.exceptions.QuantityUndefinedError
        return cast(float, self.readonly_quantity_data['qty'])

    @abc.abstractproperty
    def quantity_units(self)->str:
        raise NotImplementedError

    @property
    def quantity_is_defined(self) -> bool:
        for value in self.readonly_quantity_data.values():
            if value == None:
                return False
        return True