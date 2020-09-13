import abc
import copy
import enum
from pydiet import exceptions
from typing import TypedDict, Optional, cast

from pydiet import quantity, defining


class BulkData(TypedDict):
    pref_unit: str
    ref_qty: float
    g_per_ml: Optional[float]
    piece_mass_g: Optional[float]


def get_empty_bulk_data() -> 'BulkData':
    return BulkData(pref_unit='g',
                    ref_qty=100,
                    g_per_ml=None,
                    piece_mass_g=None)


class SupportsBulk(defining.supports_name.SupportsName):

    @abc.abstractproperty
    def _bulk_data(self) -> 'BulkData':
        raise NotImplementedError

    @property
    def readonly_bulk_data(self) -> 'BulkData':
        return copy.deepcopy(self._bulk_data)

    @property
    def pref_unit(self) -> str:
        return self.readonly_bulk_data['pref_unit']

    @property
    def ref_qty(self) -> float:
        return self.readonly_bulk_data['ref_qty']

    @property
    def g_per_ml(self) -> float:
        if not self.density_is_defined:
            raise quantity.exceptions.DensityNotConfiguredError
        return cast(float, self.readonly_bulk_data['g_per_ml'])

    @property
    def piece_mass_g(self) -> float:
        if not self.piece_mass_defined:
            raise quantity.exceptions.PcMassNotConfiguredError
        return cast(float, self.readonly_bulk_data['piece_mass_g'])

    @property
    def density_is_defined(self) -> bool:
        if self.readonly_bulk_data['g_per_ml'] == None:
            return False
        else:
            return True

    @property
    def piece_mass_defined(self) -> bool:
        if self.readonly_bulk_data['piece_mass_g'] == None:
            return False
        else:
            return True

    @property
    def piece_mass_in_pref_units(self) -> float:
        return quantity.quantity_service.convert_qty_unit(self.piece_mass_g, 'g',
                                                          self.pref_unit, self.readonly_bulk_data['g_per_ml'])

    def check_unit_configured(self, unit: str) -> bool:
        if quantity.quantity_service.unit_is_mass(unit):
            return True
        elif quantity.quantity_service.unit_is_volume(unit):
            return self.density_is_defined
        else:
            return False

    @property
    def piece_mass_summary(self) -> str:
        if self.piece_mass_defined:
            return 'One {name} is {mass:.4f}{unit}'.format(
                name=self.name,
                mass=self.piece_mass_in_pref_units,
                unit=self.pref_unit
            )
        else:
            return 'Undefined'

    @property
    def density_summary(self) -> str:
        if self.density_is_defined:
            return '{g_per_ml:.4f}g/ml'
        else:
            return 'Undefined'

    @property
    def bulk_summary(self) -> str:
        template = '''Preferred Units: {pref_unit}
Piece Mass:      {piece_mass_summary}
Density:         {density_summary}
        '''

        return template.format(
            pref_unit=self.pref_unit,
            piece_mass_summary=self.piece_mass_summary,
            density_summary=self.density_summary)


class SupportsBulkSetting(SupportsBulk):

    def set_pref_unit(self, unit: str) -> None:
        unit = quantity.quantity_service.validate_qty_unit(unit)
        if quantity.quantity_service.unit_is_volume(unit):
            if not self.density_is_defined:
                raise quantity.exceptions.DensityNotConfiguredError
        self._bulk_data['pref_unit'] = unit

    def set_ref_qty(self, qty: float) -> None:
        qty = quantity.quantity_service.validate_quantity(qty)
        self._bulk_data['ref_qty']

    def set_g_per_ml(self, g_per_ml: float) -> None:
        g_per_ml = quantity.quantity_service.validate_quantity(g_per_ml)
        self._bulk_data['g_per_ml']

    def set_piece_mass_g(self, piece_mass_g) -> None:
        piece_mass_g = quantity.quantity_service.validate_quantity(
            piece_mass_g)
        self._bulk_data['piece_mass_g']
