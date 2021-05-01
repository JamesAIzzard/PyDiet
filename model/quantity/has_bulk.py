from typing import List, TypedDict, Optional, Dict, Any

import model
import persistence


class RefQtyData(TypedDict):
    pref_unit: str
    ref_qty: float


class BulkData(RefQtyData):
    g_per_ml: Optional[float]
    piece_mass_g: Optional[float]


class HasBulk(persistence.CanLoadData):
    """Models substances with bulk properties, such as density and mass."""

    def __init__(self, bulk_data: Optional['BulkData'] = None, **kwargs):
        super().__init__(**kwargs)

        self._bulk_data: 'BulkData' = BulkData(
            pref_unit='g',
            ref_qty=100,
            g_per_ml=None,
            piece_mass_g=None
        )

        if bulk_data is not None:
            self.load_data({'bulk_data': bulk_data})

    @property
    def pref_unit(self) -> str:
        """Returns object's preferred unit of measure."""
        return self._bulk_data['pref_unit']

    @property
    def ref_qty(self) -> float:
        """Returns the object's reference quantity (in its preferred units)."""
        return self._bulk_data['ref_qty']

    @property
    def g_per_ml(self) -> float:
        """Returns the weight of 1ml of the object in g."""
        if self._bulk_data['g_per_ml'] is None:
            raise model.quantity.exceptions.UndefinedDensityError(subject=self)
        else:
            return self._bulk_data['g_per_ml']

    @property
    def piece_mass_g(self) -> float:
        """Returns the mass of a single piece of the object."""
        if self._bulk_data['piece_mass_g'] is None:
            raise model.quantity.exceptions.UndefinedPcMassError(subject=self)
        else:
            return self._bulk_data['piece_mass_g']

    @property
    def available_units(self) -> List[str]:
        """Returns a list of units which can be used on the instance."""
        units = model.quantity.MASS_UNITS
        if self.density_is_defined:
            units = units + model.quantity.VOL_UNITS
        if self.piece_mass_defined:
            units = units + model.quantity.PC_UNITS
        return units

    @property
    def ref_qty_in_g(self) -> float:
        """Return's the object's reference quantity in grams."""
        return model.quantity.convert_qty_unit(
            qty=self.ref_qty,
            start_unit=self.pref_unit,
            end_unit='g',
            g_per_ml=self.g_per_ml if self.density_is_defined else None,
            piece_mass_g=self.piece_mass_g if self.piece_mass_defined else None
        )

    @property
    def g_in_ref_qty(self) -> float:
        """Returns the number of grams in the subject's reference quantity"""
        return model.quantity.convert_qty_unit(
            qty=self.ref_qty,
            start_unit=self.pref_unit,
            end_unit='g',
            g_per_ml=self.g_per_ml if self.density_is_defined else None,
            piece_mass_g=self.piece_mass_g if self.piece_mass_defined else None
        )

    @property
    def density_is_defined(self) -> bool:
        """Returns True/False to indicate if the object's density is defined."""
        return self._bulk_data['g_per_ml'] is not None

    @property
    def piece_mass_defined(self) -> bool:
        """Returns True/False to indicate if the mass of a single piece of the substance is defined."""
        return self._bulk_data['piece_mass_g'] is not None

    def units_are_configured(self, *units) -> bool:
        """Returns True/False to indicate if the units are configured on the instance."""
        for unit in units:
            if model.quantity.units_are_volumes(unit) and not self.density_is_defined:
                return False
            if model.quantity.units_are_pieces(unit) and not self.piece_mass_defined:
                return False
        return True

    @property
    def piece_mass_in_pref_units(self) -> float:
        """Returns the mass of a single piece of the substance, in the object's preferred units."""
        return model.quantity.convert_qty_unit(
            qty=self.piece_mass_g,
            start_unit='g',
            end_unit=self.pref_unit,
            g_per_ml=self.g_per_ml if self.density_is_defined else None,
            piece_mass_g=self.piece_mass_g if self.piece_mass_defined else None
        )

    def load_data(self, data: Dict[str, Any]) -> None:
        super().load_data(data)
        if 'bulk_data' in data.keys():
            self._bulk_data = data['bulk_data']

    @property
    def persistable_data(self) -> Dict[str, Any]:
        data = super().persistable_data
        data['bulk_data'] = self._bulk_data
        return data


class HasSettableBulk(HasBulk):
    """Models substances with settable bulk properties, such as density and mass."""

    @HasBulk.ref_qty.setter
    def ref_qty(self, value: float) -> None:
        value = model.quantity.validation.validate_nonzero_quantity(value)
        self._bulk_data['ref_qty'] = value

    @HasBulk.pref_unit.setter
    def pref_unit(self, unit: str) -> None:
        """Implements pref_unit setting."""

        # Check the unit is actually valid;
        unit = model.quantity.validation.validate_qty_unit(unit)

        # Check the instance is configured to use the unit;
        if model.quantity.units_are_volumes(unit):
            if not self.density_is_defined:
                raise model.quantity.exceptions.UndefinedDensityError
        if model.quantity.units_are_pieces(unit):
            if not self.piece_mass_defined:
                raise model.quantity.exceptions.UndefinedPcMassError

        # All looks good!, set.
        self._bulk_data['pref_unit'] = unit

    @HasBulk.g_per_ml.setter
    def g_per_ml(self, g_per_ml: Optional[float]) -> None:
        """Implements gram/ml setting."""
        # If density is being unset;
        if g_per_ml is None:
            self._bulk_data['g_per_ml'] = None
        else:
            self._bulk_data['g_per_ml'] = model.quantity.validation.validate_nonzero_quantity(g_per_ml)

    def set_density(self, mass_qty: Optional[float], mass_unit: str, vol_qty: Optional[float], vol_unit: str) -> None:
        """Sets the substance's density."""
        # Unset density if we have None values;
        if mass_qty is None or vol_qty is None:
            self.g_per_ml = None
        # Dissallow zero values;
        elif vol_qty == 0 or mass_qty == 0:
            raise model.quantity.exceptions.ZeroQtyError()
        # Otherwise just set as normal;
        else:
            self.g_per_ml = model.quantity.convert_density_unit(
                qty=mass_qty / vol_qty,
                start_mass_unit=mass_unit,
                start_vol_unit=vol_unit,
                end_mass_unit='g',
                end_vol_unit='ml'
            )

    def unset_density(self) -> None:
        """Unsets the density properties on the instance."""
        self.g_per_ml = None

    @HasBulk.piece_mass_g.setter
    def piece_mass_g(self, piece_mass_g: Optional[float]) -> None:
        """Implements piece mass setting."""
        # If unsetting
        if piece_mass_g is None:
            self._bulk_data['piece_mass_g'] = None
        # All OK, go ahead;
        else:
            self._bulk_data['piece_mass_g'] = model.quantity.validation.validate_nonzero_quantity(piece_mass_g)

    def set_piece_mass(self, num_pieces: Optional[float], mass_qty: Optional[float], mass_unit: str) -> None:
        """Sets the mass of num_pieces of the substance."""
        # If we are trying to unset;
        if num_pieces is None or mass_qty is None:
            self.piece_mass_g = None
        # Dissallow zero values;
        elif num_pieces == 0 or mass_qty == 0:
            raise model.quantity.exceptions.ZeroQtyError()
        # Otherwise, set as normal;
        else:
            mass_unit = model.quantity.validation.validate_mass_unit(mass_unit)
            mass_qty = model.quantity.validation.validate_quantity(mass_qty)
            num_pieces = model.quantity.validation.validate_quantity(num_pieces)
            # Calc the mass of a single piece;
            single_pc_mass = mass_qty / num_pieces
            # Convert single piece mass to g;
            piece_mass_g = model.quantity.convert_qty_unit(
                single_pc_mass, mass_unit, 'g')

            self.piece_mass_g = piece_mass_g

    def unset_piece_mass(self) -> None:
        """Unsets the piece mass data on the instance."""
        self.piece_mass_g = None
