"""Functionality associated with extended units in the model.
"""
import abc
import copy
from typing import List, Optional, Dict, Any

import model
import persistence


class HasReadableExtendedUnits(persistence.YieldsPersistableData, abc.ABC):
    """Implements functionality associated with readable extended units."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    @abc.abstractmethod
    def _g_per_ml(self) -> Optional[float]:
        """Subclass implementation to return grams per ml if defined, or None if not."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def _piece_mass_g(self) -> Optional[float]:
        """Subclass implementation to return grams per ml if defined, or None if not."""
        raise NotImplementedError

    @property
    def g_per_ml(self) -> float:
        """Gets the weight of a millilitre of the substance in grams."""
        if self._g_per_ml is None:
            raise model.quantity.exceptions.UndefinedDensityError(subject=self)
        else:
            return self._g_per_ml

    @property
    def piece_mass_g(self) -> float:
        """Gets the weight of a single piece of the subtance."""
        if self._piece_mass_g is None:
            raise model.quantity.exceptions.UndefinedPcMassError(subject=self)
        else:
            return self._piece_mass_g

    @property
    def density_is_defined(self) -> bool:
        """Returns True/False to indicate if the object's density is defined."""
        return self._g_per_ml is not None

    @property
    def piece_mass_is_defined(self) -> bool:
        """Returns True/False to indicate if the mass of a single piece of the substance is defined."""
        return self._piece_mass_g is not None

    @property
    def available_units(self) -> List[str]:
        """Returns a list of units which can be used when quantifying the substance."""
        # Create a copy of the global units list (we don't want to accidentaly change the globals);
        units = copy.copy(model.quantity.MASS_UNITS)
        if self.density_is_defined:
            units += copy.copy(model.quantity.VOL_UNITS)
        if self.piece_mass_is_defined:
            units += copy.copy(model.quantity.PC_UNITS)
        return units

    def units_are_configured(self, *units) -> bool:
        """Returns True/False to indicate if the units are configured on the instance."""
        for unit in units:
            # First, check the unit is recognised;
            unit = model.quantity.validation.validate_qty_unit(unit)

            # Check volumes;
            if model.quantity.units_are_volumes(unit) and not self.density_is_defined:
                return False

            # Check pieces;
            if model.quantity.units_are_pieces(unit) and not self.piece_mass_is_defined:
                return False

        return True

    @property
    def persistable_data(self) -> Dict[str, Any]:
        """Returns the persistable data to include extended units data."""
        data = super().persistable_data
        data['extended_units_data'] = model.quantity.ExtendedUnitsData(
            g_per_ml=self._g_per_ml,
            piece_mass_g=self._piece_mass_g
        )
        return data


class HasSettableExtendedUnits(HasReadableExtendedUnits, persistence.CanLoadData):
    """Implements functionality associated with settable extended units."""

    def __init__(self, extended_units_data: Optional['model.quantity.ExtendedUnitsData'] = None, **kwargs):
        super().__init__(**kwargs)

        # Now we are storing data locally on the instance, so create somewhere to put it.
        self._extended_units_data: 'model.quantity.ExtendedUnitsData' = model.quantity.ExtendedUnitsData(
            g_per_ml=None,
            piece_mass_g=None
        )

        # If we got data, then load it up;
        if extended_units_data is not None:
            self.load_data({'extended_units_data': extended_units_data})

    @property
    def _g_per_ml(self) -> Optional[float]:
        """Returns the grams per ml for the instance, if defined, None if not."""
        return self._extended_units_data['g_per_ml']

    @property
    def _piece_mass_g(self) -> Optional[float]:
        """Returns the peice mass in grams for the instance, if defined, None if not."""
        return self._extended_units_data['piece_mass_g']

    @HasReadableExtendedUnits.g_per_ml.setter
    def g_per_ml(self, g_per_ml: Optional[float]) -> None:
        """Implements gram/ml setting."""
        # If density is being unset;
        if g_per_ml is None:
            self._extended_units_data['g_per_ml'] = None
        else:
            self._extended_units_data['g_per_ml'] = model.quantity.validation.validate_nonzero_quantity(g_per_ml)

    def set_density(self, mass_qty: float, mass_unit: str, vol_qty: float, vol_unit: str) -> None:
        """Sets the substance's density."""
        # Catch None values, we should be using the special unsetter function;
        if mass_qty is None or vol_qty is None:
            raise model.quantity.exceptions.InvalidQtyError(
                quantity=None,
                subject=self
            )
        # Otherwise just set as normal;
        else:
            # Validate the mass and volume qty;
            mass_qty = model.quantity.validation.validate_nonzero_quantity(mass_qty)
            vol_qty = model.quantity.validation.validate_nonzero_quantity(vol_qty)
            self.g_per_ml = model.quantity.convert_density_unit(
                qty=mass_qty / vol_qty,
                start_mass_unit=mass_unit,
                start_vol_unit=vol_unit,
                end_mass_unit='g',
                end_vol_unit='ml'
            )

    def unset_density(self) -> None:
        """Unsets the substance's density."""
        self._extended_units_data['g_per_ml'] = None

    @HasReadableExtendedUnits.piece_mass_g.setter
    def piece_mass_g(self, piece_mass_g: Optional[float]) -> None:
        """Implements piece mass setting."""
        # If unsetting
        if piece_mass_g is None:
            self._extended_units_data['piece_mass_g'] = None
        # All OK, go ahead;
        else:
            self._extended_units_data['piece_mass_g'] = model.quantity.validation.validate_nonzero_quantity(
                piece_mass_g)

    def set_piece_mass(self, num_pieces: Optional[float], mass_qty: Optional[float], mass_unit: str) -> None:
        """Sets the mass of num_pieces of the substance."""
        # If we are trying to unset, raise an exception, we should use the special
        # unsetter function;
        if num_pieces is None or mass_qty is None:
            raise model.quantity.exceptions.InvalidQtyError(
                quantity=None,
                subject=self
            )
        # Catch divide by zero;
        elif num_pieces == 0:
            raise model.quantity.exceptions.ZeroQtyError()
        # Otherwise, set as normal;
        else:
            mass_unit = model.quantity.validation.validate_mass_unit(mass_unit)
            mass_qty = model.quantity.validation.validate_nonzero_quantity(mass_qty)
            num_pieces = model.quantity.validation.validate_nonzero_quantity(num_pieces)
            # Calc the mass of a single piece;
            single_pc_mass = mass_qty / num_pieces
            # Convert single piece mass to g;
            piece_mass_g = model.quantity.convert_qty_unit(
                single_pc_mass, mass_unit, 'g')

            # Go ahead and set;
            self.piece_mass_g = piece_mass_g

    def unset_piece_mass(self) -> None:
        """Unsets the substance's piece mass."""
        self._extended_units_data['piece_mass_g'] = None

    def load_data(self, data: Dict[str, Any]) -> None:
        """Loads the extended units data from the data dict into the instance."""
        # Pass data on to superclass loaders;
        super().load_data(data)

        # If there is a key for extended units, load it;
        # Pass it through the setters to catch any invalid values;
        if 'extended_units_data' in data.keys():
            if data['extended_units_data']['g_per_ml'] is not None:
                self.set_density(
                    mass_qty=data['extended_units_data']['g_per_ml'],
                    mass_unit='g',
                    vol_qty=1,
                    vol_unit='ml'
                )
            if data['extended_units_data']['piece_mass_g'] is not None:
                self.set_piece_mass(
                    mass_qty=data['extended_units_data']['piece_mass_g'],
                    mass_unit='g',
                    num_pieces=1
                )
