import abc
from typing import Optional, Dict, Union, cast

from pydiet import quantity

density_data_template = {
    'g_per_ml' : None,
    'pref_vol_units' : None
}

class SupportsDensity(abc.ABC):

    @abc.abstractproperty
    def readonly_density_data(self) -> Dict[str, Union[float, str]]:
        raise NotImplementedError

    @property
    def g_per_ml(self) -> float:
        if not self.density_is_defined:
            raise quantity.exceptions.DensityDataUndefinedError
        return cast(float, self.readonly_density_data['g_per_ml'])
 
    @property
    def pref_vol_units(self) -> str:
        if not self.density_is_defined:
            raise quantity.exceptions.DensityDataUndefinedError
        return cast(str, self.readonly_density_data['pref_vol_units'])

    @property
    def density_is_defined(self) -> bool:
        for value in self.readonly_density_data.values():
            if value == None:
                return False
        return True