import abc
from typing import TypedDict, Optional

from pydiet import quantity
from pydiet.name import HasName
from pydiet.quantity import exceptions, validation


class BulkData(TypedDict):
    pref_unit: str
    ref_qty: float
    g_per_ml: Optional[float]
    piece_mass_g: Optional[float]


class HasBulk(HasName, abc.ABC):
    """Models substances with bulk properties, such as density and mass."""

    def __init__(self, pref_unit: str = 'g', ref_qty: float = 100, g_per_ml: Optional[float] = None,
                 piece_mass_g: Optional[float] = None, **kwargs):
        super().__init__(**kwargs)
        self._pref_unit: str = pref_unit
        self._ref_qty: float = ref_qty
        self._g_per_ml: float = g_per_ml
        self._piece_mass_g: float = piece_mass_g

    @property
    def pref_unit(self) -> str:
        """Returns object's preferred unit of measure."""
        return self._pref_unit

    def _set_pref_unit(self, unit: str) -> None:
        """Pref unit setter implementation."""
        raise exceptions.BulkNotSettableError

    @pref_unit.setter
    def pref_unit(self, unit: str) -> None:
        """Sets the pref unit."""
        self._set_pref_unit(unit)

    @property
    def ref_qty(self) -> float:
        """Returns the object's reference quantity (in its preferred units)."""
        return self._ref_qty

    def _set_ref_quantity(self, qty: float) -> None:
        """Ref quantity setter implementation."""
        raise exceptions.BulkNotSettableError

    @ref_qty.setter
    def ref_qty(self, qty: float) -> None:
        """Sets the object's reference quantity."""
        self._set_ref_quantity(qty)

    @property
    def ref_qty_in_g(self) -> float:
        """Return's the object's reference quantity in grams."""
        return quantity.convert_qty_unit(self.ref_qty, self.pref_unit, 'g', self.g_per_ml, self.piece_mass_g)

    @property
    def g_per_ml(self) -> Optional[float]:
        """Returns the weight of 1ml of the object in g."""
        return self._g_per_ml

    def _set_g_per_ml(self, g_per_ml: Optional[float]) -> None:
        """Grams/ml setter implementation."""
        raise exceptions.BulkNotSettableError

    @g_per_ml.setter
    def g_per_ml(self, g_per_ml: Optional[float]) -> None:
        """Set's the object's grams/ml value."""
        self._set_g_per_ml(g_per_ml)

    @property
    def piece_mass_g(self) -> Optional[float]:
        """Returns the mass of a single piece of the object."""
        return self._piece_mass_g

    def _set_piece_mass_g(self, piece_mass_g: Optional[float]) -> None:
        """Piece mass setter implementation."""
        raise exceptions.BulkNotSettableError

    @piece_mass_g.setter
    def piece_mass_g(self, piece_mass_g: Optional[float]) -> None:
        """Sets the mass of a single piece of the object."""
        self._set_piece_mass_g(piece_mass_g)

    @property
    def density_is_defined(self) -> bool:
        """Returns True/False to indicate if the object's density is defined."""
        return self.g_per_ml is None

    @property
    def piece_mass_defined(self) -> bool:
        """Returns True/False to indicate if the mass of a single piece of the substance is defined."""
        return self.piece_mass_g is None

    @property
    def piece_mass_in_pref_units(self) -> float:
        """Returns the mass of a single piece of the substance, in the object's preferred units."""
        return quantity.convert_qty_unit(qty=self.piece_mass_g,
                                         start_unit='g',
                                         end_unit=self.pref_unit,
                                         g_per_ml=self.g_per_ml,
                                         piece_mass_g=self.piece_mass_g)

    @property
    def bulk_data(self) -> 'BulkData':
        """Returns a dictionary of all the substance's bulk data fields."""
        return BulkData(pref_unit=self.pref_unit,
                        ref_qty=self.ref_qty,
                        g_per_ml=self.g_per_ml,
                        piece_mass_g=self.piece_mass_g)

    def check_units_configured(self, *units: str) -> bool:
        """Returns True/False to indicate if the specified units have been configured on, and can therefore
        be used with the substance instance."""
        for unit in units:
            if quantity.units_are_volumes(unit):
                if not self.density_is_defined:
                    return False
            elif quantity.units_are_pieces(unit):
                if not self.piece_mass_defined:
                    return False
        return True

    @property
    def piece_mass_summary(self) -> str:
        """Returns a readable summary of the mass of a single piece of the substance."""
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
        """Returns a readable summary of the density of the substance."""
        if self.density_is_defined:
            return '{g_per_ml:.2f}g/ml'.format(g_per_ml=self.g_per_ml)
        else:
            return 'Undefined'

    @property
    def ref_amount_summary(self) -> str:
        """Returns a readable summary of the substance's reference amount."""
        return '{ref_qty}{ref_unit}'.format(
            ref_qty=self.ref_qty,
            ref_unit=self.pref_unit)

    @property
    def bulk_summary(self) -> str:
        """Returns a readable summary of all of the substance's bulk data."""
        template = '''Reference Amount: {ref_amount_summary}
Piece Mass:       {piece_mass_summary}
Density:          {density_summary}
        '''

        return template.format(
            ref_amount_summary=self.ref_amount_summary,
            piece_mass_summary=self.piece_mass_summary,
            density_summary=self.density_summary)


class SupportsBulkSetting(HasBulk, abc.ABC):
    """Models substances with settable bulk properties, such as density and mass."""

    @abc.abstractmethod
    def _density_reset_cleanup(self) -> None:
        """Does any custom density data/reference removal on the instance."""
        raise NotImplementedError

    @abc.abstractmethod
    def _piece_mass_reset_cleanup(self) -> None:
        """Does any custom piece mass data/reference removal on the instance."""
        raise NotImplementedError

    def _set_pref_unit(self, unit: str) -> None:
        """Implements pref_unit setting."""

        # Check the unit is actually valid;
        unit = validation.validate_qty_unit(unit)

        # Check the instance is configured to use the unit;
        if quantity.units_are_volumes(unit):
            if not self.density_is_defined:
                raise exceptions.DensityNotConfiguredError
        if quantity.units_are_pieces(unit):
            if not self.piece_mass_defined:
                raise exceptions.PcMassNotConfiguredError

        self._pref_unit = unit

    def _set_g_per_ml(self, g_per_ml: Optional[float]) -> None:
        """Implements gram/ml setting."""
        if g_per_ml is None:
            self._density_reset_cleanup()
            self._g_per_ml = None
        else:
            self._g_per_ml = validation.validate_quantity(g_per_ml)

    def set_density(self, mass_qty: float, mass_unit: str, vol_qty: float, vol_unit: str) -> None:
        """Sets the substance's density."""
        self.g_per_ml = quantity.convert_density_unit(
            qty=mass_qty / vol_qty,
            start_mass_unit=mass_unit,
            start_vol_unit=vol_unit,
            end_mass_unit='g',
            end_vol_unit='ml',
            piece_mass_g=self.piece_mass_g
        )

    def _set_piece_mass_g(self, piece_mass_g: Optional[float]) -> None:
        """Implements piece mass setting."""
        if piece_mass_g is None:
            self._piece_mass_reset_cleanup()
            self._piece_mass_g = None
        else:
            self._piece_mass_g = validation.validate_quantity(piece_mass_g)

    def set_piece_mass(self, num_pieces: float, mass_qty: float, mass_unit: str) -> None:
        """Sets the mass of num_pieces of the substance."""
        mass_unit = validation.validate_mass_unit(mass_unit)
        mass_qty = validation.validate_quantity(mass_qty)
        num_pieces = validation.validate_quantity(num_pieces)
        # Calc the mass of a single piece;
        single_pc_mass = mass_qty / num_pieces
        # Convert single piece mass to g;
        piece_mass_g = quantity.convert_qty_unit(
            single_pc_mass, mass_unit, 'g')

        self._piece_mass_g = piece_mass_g
