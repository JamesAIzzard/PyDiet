import abc
from abc import abstractmethod
import copy
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

    def check_units_configured(self, *units: str) -> bool:
        for unit in units:
            if quantity.quantity_service.units_are_volumes(unit):
                if not self.density_is_defined:
                    return False
            elif quantity.quantity_service.units_are_pieces(unit):
                if not self.piece_mass_defined:
                    return False
        return True

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
            return '{g_per_ml:.4f}g/ml'.format(g_per_ml=self.g_per_ml)
        else:
            return 'Undefined'

    @property
    def bulk_summary(self) -> str:
        template = '''Reference Amount: {ref_qty}{pref_unit}
Piece Mass:       {piece_mass_summary}
Density:          {density_summary}
        '''

        return template.format(
            ref_qty=self.ref_qty,
            pref_unit=self.pref_unit,
            piece_mass_summary=self.piece_mass_summary,
            density_summary=self.density_summary)


class SupportsBulkSetting(SupportsBulk):

    @abstractmethod
    def _density_reset_cleanup(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def _piece_mass_reset_cleanup(self) -> None:
        raise NotImplementedError

    def set_bulk_data(self, bulk_data: 'BulkData') -> None:
        self.set_pref_unit(bulk_data['pref_unit'])
        self.set_ref_qty(bulk_data['ref_qty'])
        self.set_g_per_ml(bulk_data['g_per_ml'])
        self.set_piece_mass_g(bulk_data['piece_mass_g'])

    def set_pref_unit(self, unit: str) -> None:
        unit = quantity.quantity_service.validate_qty_unit(unit)
        if quantity.quantity_service.units_are_volumes(unit):
            if not self.density_is_defined:
                raise quantity.exceptions.DensityNotConfiguredError
        if quantity.quantity_service.units_are_pieces(unit):
            if not self.density_is_defined:
                raise quantity.exceptions.PcMassNotConfiguredError
        self._bulk_data['pref_unit'] = unit

    def set_ref_qty(self, qty: float) -> None:
        qty = quantity.quantity_service.validate_quantity(qty)
        self._bulk_data['ref_qty'] = qty

    def set_g_per_ml(self, g_per_ml: Optional[float]) -> None:
        if not g_per_ml == None:
            g_per_ml = quantity.quantity_service.validate_quantity(g_per_ml)
        self._bulk_data['g_per_ml'] = g_per_ml

    def set_density(self, mass_qty: float, mass_unit: str, vol_qty: float, vol_unit: str) -> None:
        g_per_ml = quantity.quantity_service.convert_density_unit(
            qty=mass_qty/vol_qty,
            start_mass_unit=mass_unit,
            start_vol_unit=vol_unit,
            end_mass_unit='g',
            end_vol_unit='ml',
            piece_mass_g=self.readonly_bulk_data['piece_mass_g']
        )
        self.set_g_per_ml(g_per_ml)

    def reset_density(self) -> None:
        self._density_reset_cleanup()
        self._bulk_data['g_per_ml'] = None

    def set_piece_mass_g(self, piece_mass_g: Optional[float]) -> None:
        if not piece_mass_g == None:
            piece_mass_g = quantity.quantity_service.validate_quantity(
                piece_mass_g)
        self._bulk_data['piece_mass_g'] = piece_mass_g

    def set_piece_mass(self, num_pieces: float, mass_qty: float, mass_unit: str) -> None:
        mass_unit = quantity.quantity_service.validate_mass_unit(mass_unit)
        mass_qty = quantity.quantity_service.validate_quantity(mass_qty)
        num_pieces = quantity.quantity_service.validate_quantity(num_pieces)
        # Calc the mass of a single piece;
        single_pc_mass = mass_qty/num_pieces
        # Convert single piece mass to g;
        piece_mass_g = quantity.quantity_service.convert_qty_unit(
            single_pc_mass, mass_unit, 'g')
        # Set;
        self.set_piece_mass_g(piece_mass_g)

    def reset_piece_mass(self):
        self._piece_mass_reset_cleanup()
        self.set_piece_mass_g(None)

    def reset_bulk(self) -> None:
        self.set_bulk_data(get_empty_bulk_data())
        self.reset_density()
        self.reset_piece_mass()
