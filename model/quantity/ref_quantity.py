from typing import TypedDict, Callable, Optional

import model
import persistence


class RefQtyData(TypedDict):
    pref_unit: str
    ref_qty: float


class RefQuantity(persistence.CanLoadData):
    """Models a reference quantity of substance.
    Accepts callback functions to determine if it can get and set density and peice units.
    Uses callback functions to reset a reference quantity which uses a unit which is not configured.
    This is important, because we need to be able to recover if the substance has its density or
    piece mass undefined without changing the reference quantity here.
    """

    def __init__(self,
                 can_use_density_units: Callable[[], bool],
                 can_use_piece_units: Callable[[], bool],
                 data: Optional['RefQtyData'] = None):

        self._can_use_density_units = can_use_density_units
        self._can_use_piece_units = can_use_piece_units
        self._data: 'RefQtyData' = RefQtyData(
            pref_unit='g',
            ref_qty=100
        )

        if data is not None:
            self.load_data(data)

    def _validate_units(self) -> None:
        if model.quantity.units_are_pieces(self._data['pref_unit']) and not self._can_use_piece_units:
            raise model.quantity.exceptions.UndefinedPcMassError()
        elif model.quantity.units_are_volumes(self._data['pref_unit']) and not self._can_use_density_units:
            raise model.quantity.exceptions.UndefinedDensityError()

    def _reset_unit(self) -> None:
        """Resets the ref quantity to default."""
        self._data['pref_unit'] = 'g'
        self._data['ref_qty'] = 100

    @property
    def pref_unit(self) -> str:
        """Gets the preferred unit."""
        # Silently recover if the right units are not configured;
        try:
            self._validate_units()
        except model.quantity.exceptions.UnitNotConfiguredError:
            self._reset_unit()
        # Go ahead and return
        return self._data['pref_unit']

    @property
    def ref_qty(self) -> float:
        """Gets the reference quantity."""
        # Silently recover if the right units are not configured;
        try:
            self._validate_units()
        except model.quantity.exceptions.UnitNotConfiguredError:
            self._reset_unit()
        # Go ahead and return
        return self._data['ref_qty']

    def load_data(self, data: 'RefQtyData') -> None:
        self._data = data
        # Silently recover if the right units are not configured;
        try:
            self._validate_units()
        except model.quantity.exceptions.UnitNotConfiguredError:
            self._reset_unit()

    @property
    def persistable_data(self) -> 'RefQtyData':
        # Silently recover if the right units are not configured;
        try:
            self._validate_units()
        except model.quantity.exceptions.UnitNotConfiguredError:
            self._reset_unit()
        return self._data


class SettableRefQuantity(RefQuantity):
    """Settable version of the reference quantity."""

    @RefQuantity.ref_qty.setter
    def ref_qty(self, value: float) -> None:
        """Sets the reference quantity."""
        self._data['ref_qty'] = model.quantity.validation.validate_nonzero_quantity(value)

    @RefQuantity.pref_unit.setter
    def pref_unit(self, unit: str) -> None:
        """Sets the preferred unit."""
        # First, make sure the unit is recognised;
        unit = model.quantity.validation.validate_qty_unit(unit)

        # If it is a volume unit, make sure we have density configured;
        if model.quantity.units_are_volumes(unit) and not self._can_use_density_units():
            raise model.quantity.exceptions.UndefinedDensityError()

        # If it is a piece mass unit, make sure we have piece mass configured;
        if model.quantity.units_are_pieces(unit) and not self._can_use_piece_units():
            raise model.quantity.exceptions.UndefinedPcMassError()

        # All must be OK, go ahead and set;
        self._data['pref_unit'] = unit
