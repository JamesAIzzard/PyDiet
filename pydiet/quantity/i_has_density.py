import abc
from typing import Dict, Union, cast

from pydiet import quantity

data_template = {
    "mass": None,
    "mass_units": None,
    "vol": None,
    "vol_units": None
}

class IHasDensity(abc.ABC):

    @abc.abstractproperty
    def density_data(self) -> Dict[str, Union[str, float]]:
        raise NotImplementedError

    @property
    def density_is_defined(self) -> bool:
        for value in self.density_data.values():
            if value == None: return False
        return True

    @property
    def density_g_per_ml(self) -> float:
        # Catch density not being defined;
        if not self.density_is_defined:
            raise quantity.exceptions.DensityUndefinedError
        # Convert mass component to grams;
        mass_g = quantity.quantity_service.convert_mass_units(
            cast(float, self.density_data['mass']),
            cast(str, self.density_data['mass_units']),
            'g'
        )
        # Convert vol component to ml;
        vol_ml = quantity.quantity_service.convert_volume_units(
            cast(float, self.density_data['vol']),
            cast(str, self.density_data['vol_units']),
            'ml'
        )
        # Return g/ml;
        return mass_g/vol_ml        