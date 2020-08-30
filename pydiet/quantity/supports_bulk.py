import abc
from typing import TypedDict, Optional, cast

from pydiet import quantity


class DensityData(TypedDict):
    g_per_ml: Optional[float]
    pref_vol_units: Optional[str]


class UnitMassData(TypedDict):
    unit_mass_g: Optional[float]
    pref_unit_mass_units: Optional[str]


class BulkData(TypedDict):
    g_per_ml: Optional[float]
    pref_vol_units: Optional[str]
    unit_mass_g: Optional[float]
    pref_unit_mass_units: Optional[str]

def get_empty_bulk_data() -> 'BulkData':
    return BulkData(g_per_ml=None,
                    pref_vol_units=None,
                    unit_mass_g=None,
                    pref_unit_mass_units=None)


class SupportsBulk(abc.ABC):

    @abc.abstractproperty
    def _bulk_data(self) -> 'BulkData':
        raise NotImplementedError

    @property
    def readonly_density_data(self) -> 'DensityData':
        density_data: 'DensityData' = {
            'g_per_ml': self._bulk_data['g_per_ml'],
            'pref_vol_units': self._bulk_data['pref_vol_units']
        }
        return density_data

    @property
    def bulk_summary(self) -> str:
        return 'A bulk summary.'

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

    @property
    def readonly_unit_mass_data(self) -> 'UnitMassData':
        unit_mass_data: 'UnitMassData' = {
            'unit_mass_g': self._bulk_data['unit_mass_g'],
            'pref_unit_mass_units': self._bulk_data['pref_unit_mass_units']
        }
        return unit_mass_data

    @property
    def unit_mass_defined(self) -> bool:
        for value in self.readonly_unit_mass_data.values():
            if value == None:
                return False
        return True

    @property
    def unit_mass_g(self) -> float:
        if not self.unit_mass_defined:
            raise quantity.exceptions.UnitMassUndefinedError
        return cast(float, self.readonly_unit_mass_data['unit_mass_g'])

    @property
    def pref_unit_mass_units(self) -> str:
        if not self.unit_mass_defined:
            raise quantity.exceptions.UnitMassUndefinedError
        return cast(str, self.readonly_unit_mass_data['pref_unit_mass_units'])


class SupportsBulkSetting(SupportsBulk):

    def set_density(self, g_per_ml: float, pref_vol_units: str) -> None:
        # Validate things;
        g_per_ml = quantity.quantity_service.validate_quantity(g_per_ml)
        pref_vol_units = quantity.quantity_service.validate_vol_unit(
            pref_vol_units)
        # Update;
        self._bulk_data['g_per_ml'] = g_per_ml
        self._bulk_data['pref_vol_units'] = pref_vol_units

    def set_unit_mass_data(self, unit_mass_g: float, unit_mass_pref_units: str) -> None:
        # Validate;
        unit_mass_g = quantity.quantity_service.validate_quantity(unit_mass_g)
        unit_mass_pref_units = quantity.quantity_service.validate_qty_unit(
            unit_mass_pref_units)
        # Update values;
        self._bulk_data['unit_mass_g'] = unit_mass_g
        self._bulk_data['pref_unit_mass_units'] = unit_mass_pref_units
