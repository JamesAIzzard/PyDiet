import abc
from typing import Optional, TypedDict, Protocol

from pydiet import quantity


class DensityData(TypedDict):
    g_per_ml: Optional[float]
    pref_vol_units: Optional[str]


density_data_template:'DensityData' = {
    'g_per_ml': None,
    'pref_vol_units': None
}


class SupportsDensity(Protocol):

    @abc.abstractproperty
    def readonly_density_data(self) -> 'DensityData':
        raise NotImplementedError

    @property
    def g_per_ml(self) -> float:
        if not self.density_is_defined:
            raise quantity.exceptions.DensityDataUndefinedError
        return self.readonly_density_data['g_per_ml']

    @property
    def pref_vol_units(self) -> str:
        if not self.density_is_defined:
            raise quantity.exceptions.DensityDataUndefinedError
        return self.readonly_density_data['pref_vol_units']

    @property
    def density_is_defined(self) -> bool:
        for value in self.readonly_density_data.values():
            if value == None:
                return False
        return True

class SupportsDensitySetting(SupportsDensity, Protocol):

    @abc.abstractproperty
    def density_data(self) -> 'DensityData':
        raise NotImplementedError

    def set_g_per_ml(self, value:float) -> None:
        self.density_data['g_per_ml'] = value