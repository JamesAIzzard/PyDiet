import abc
import copy
from typing import TypedDict, Optional

from pydiet import quantity


class BulkData(TypedDict):
    pref_unit: str
    ref_qty: float
    g_per_ml: Optional[float]
    piece_mass_g: Optional[float]


def get_empty_bulk_data() -> BulkData:
    return BulkData(pref_unit='g',
                    ref_qty=100,
                    g_per_ml=None,
                    piece_mass_g=None)


class SupportsBulk:

    @property
    @abc.abstractmethod
    def _bulk_data(self) -> 'BulkData':
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    def bulk_data(self) -> 'BulkData':
        return copy.deepcopy(self._bulk_data)

    @property
    def pref_unit(self) -> str:
        return self.bulk_data['pref_unit']

    @property
    def ref_unit(self) -> str:
        """Alias for pref_unit"""
        return self.pref_unit

    @property
    def ref_qty(self) -> float:
        return self.bulk_data['ref_qty']

    @property
    def ref_qty_in_g(self) -> float:
        return quantity.quantity_service.convert_qty_unit(self.ref_qty, self.pref_unit, 'g', self.g_per_ml,
                                                          self.piece_mass_g)

    @property
    def g_per_ml(self) -> Optional[float]:
        return self.bulk_data['g_per_ml']

    @property
    def piece_mass_g(self) -> Optional[float]:
        return self.bulk_data['piece_mass_g']

    @property
    def density_is_defined(self) -> bool:
        if self.bulk_data['g_per_ml'] is None:
            return False
        else:
            return True

    @property
    def piece_mass_defined(self) -> bool:
        if self.bulk_data['piece_mass_g'] is None:
            return False
        else:
            return True

    @property
    def piece_mass_in_pref_units(self) -> float:
        return quantity.quantity_service.convert_qty_unit(self.piece_mass_g, 'g', self.pref_unit, self.g_per_ml,
                                                          self.piece_mass_g)

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
            return 'One {name} is {mass:.2f}g'.format(
                name=self.name,
                mass=self.piece_mass_g,
                unit=self.pref_unit
            )
        else:
            return 'Undefined'

    @property
    def density_summary(self) -> str:
        if self.density_is_defined:
            return '{g_per_ml:.2f}g/ml'.format(g_per_ml=self.g_per_ml)
        else:
            return 'Undefined'

    @property
    def ref_amount_summary(self) -> str:
        return '{ref_qty}{ref_unit}'.format(
            ref_qty=self.ref_qty,
            ref_unit=self.ref_unit)

    @property
    def bulk_summary(self) -> str:
        template = '''Reference Amount: {ref_amount_summary}
Piece Mass:       {piece_mass_summary}
Density:          {density_summary}
        '''

        return template.format(
            ref_amount_summary=self.ref_amount_summary,
            piece_mass_summary=self.piece_mass_summary,
            density_summary=self.density_summary)


class SupportsBulkSetting(SupportsBulk):
    @property
    def bulk_data(self) -> 'BulkData':
        return self._bulk_data

    @abc.abstractmethod
    def _density_reset_cleanup(self) -> None:
        """Does any custom density data/reference removal on the instance."""
        raise NotImplementedError

    @abc.abstractmethod
    def _piece_mass_reset_cleanup(self) -> None:
        """Does any custom piece mass data/reference removal on the instance."""
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
            if not self.piece_mass_defined:
                raise quantity.exceptions.PcMassNotConfiguredError
        self.bulk_data['pref_unit'] = unit

    def set_ref_unit(self, unit: str) -> None:
        """Alias for set_pref_unit"""
        self.set_pref_unit(unit)

    def set_ref_qty(self, qty: float) -> None:
        qty = quantity.quantity_service.validate_quantity(qty)
        self.bulk_data['ref_qty'] = qty

    def set_g_per_ml(self, g_per_ml: Optional[float]) -> None:
        if g_per_ml is not None:
            g_per_ml = quantity.quantity_service.validate_quantity(g_per_ml)
        self.bulk_data['g_per_ml'] = g_per_ml

    def set_density(self, mass_qty: float, mass_unit: str, vol_qty: float, vol_unit: str) -> None:
        g_per_ml = quantity.quantity_service.convert_density_unit(
            qty=mass_qty / vol_qty,
            start_mass_unit=mass_unit,
            start_vol_unit=vol_unit,
            end_mass_unit='g',
            end_vol_unit='ml',
            piece_mass_g=self.piece_mass_g
        )
        self.set_g_per_ml(g_per_ml)

    def reset_density(self) -> None:
        self._density_reset_cleanup()
        self.set_g_per_ml(None)

    def set_piece_mass_g(self, piece_mass_g: Optional[float]) -> None:
        if piece_mass_g is not None:
            piece_mass_g = quantity.quantity_service.validate_quantity(piece_mass_g)
        self.bulk_data['piece_mass_g'] = piece_mass_g

    def set_piece_mass(self, num_pieces: float, mass_qty: float, mass_unit: str) -> None:
        mass_unit = quantity.quantity_service.validate_mass_unit(mass_unit)
        mass_qty = quantity.quantity_service.validate_quantity(mass_qty)
        num_pieces = quantity.quantity_service.validate_quantity(num_pieces)
        # Calc the mass of a single piece;
        single_pc_mass = mass_qty / num_pieces
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
