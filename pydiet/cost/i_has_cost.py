import abc
from typing import Dict, Union, cast

data_template = {
    "cost": None,
    "qty": None,
    "qty_units": None
}

class IHasCost(abc.ABC):

    @abc.abstractproperty
    def cost_data(self) ->Dict[str, Union[str, float]]:
        raise NotImplementedError   

    @property
    def cost_is_defined(self) -> bool:
        for value in self.cost_data.values():
            if value == None:
                return False
        return True