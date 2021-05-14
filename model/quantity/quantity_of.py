from typing import TypedDict, Optional, Any, Callable

import model
import persistence


class QuantityData(TypedDict):
    quantity_in_g: Optional[float]
    pref_unit: str


class QuantityOf(model.SupportsDefinition, persistence.YieldsPersistableData):
    """Models a quantity of a substance.
    Since this quantity may come from anywhere, it is not stored locally. This class
    may also be instantiated directly, so we can't rely on an abstract class.
    Instead we take advantage of closures and pass in a callback as a data source.
    """

    def __init__(self, subject: Any, quantity_data_src: Callable[[], 'QuantityData'], **kwargs):
        super().__init__(**kwargs)

        # Stash the subject;
        self._subject = subject

        # Stash the data source callable;
        self._quantity_data_src = quantity_data_src

    @property
    def subject(self) -> Any:
        """Returns the subject whos quantity is being described."""
        return self._subject

    @property
    def quantity_in_g(self) -> float:
        """Returns the object's quantity in grams."""
        _qty_in_g = self._quantity_data_src()['quantity_in_g']
        if _qty_in_g is None:
            raise model.quantity.exceptions.UndefinedQuantityError()
        else:
            return _qty_in_g

    def _validate_pref_unit(self, unit: str) -> str:
        # First, check the unit is known by the system;
        unit = model.quantity.validation.validate_qty_unit(unit)

        # If the subject doesn't support extended units, and the unit is a mass or volume;
        if model.quantity.unit_is_extended(unit) \
                and not isinstance(self._subject, model.quantity.SupportsExtendedUnits):
            raise model.quantity.exceptions.UnsupportedExtendedUnitsError(subject=self)

        # OK, so the subject does support extended units;
        # If the unit is a volume, and the subject doesn't have density defined;
        if model.quantity.units_are_volumes(unit) and not self._subject.density_is_defined:
            raise model.quantity.exceptions.UndefinedDensityError(subject=self.subject)
        elif model.quantity.units_are_pieces(unit) and not self._subject.piece_mass_defined:
            raise model.quantity.exceptions.UndefinedPcMassError(subject=self.subject)

        # OK, return the unit;
        return unit

    @property
    def pref_unit(self) -> str:
        """Returns the unit used to define the subject quantity."""
        # Return the validated unit
        return self._validate_pref_unit(self._quantity_data_src()['pref_unit'])

    @property
    def ref_qty(self) -> float:
        """Returns the reference quantity used to define the subject quantity."""
        g_per_ml = None
        piece_mass_g = None
        if isinstance(self.subject, model.quantity.SupportsExtendedUnits):
            g_per_ml = self.subject.g_per_ml if self.subject.density_is_defined else None
            piece_mass_g = self.subject.piece_mass_g if self.subject.piece_mass_defined else None
        return model.quantity.convert_qty_unit(
            qty=self.quantity_in_g,
            start_unit='g',
            end_unit=self.pref_unit,
            g_per_ml=g_per_ml,
            piece_mass_g=piece_mass_g
        )

    @property
    def is_defined(self) -> bool:
        return self._quantity_data_src()['quantity_in_g'] is not None

    @property
    def persistable_data(self) -> 'QuantityData':
        return self._quantity_data_src()


class SettableQuantityOf(QuantityOf, persistence.CanLoadData):
    """Models a settable quantity of substance."""

    def __init__(self, quantity_data: Optional['QuantityData'] = None, **kwargs):
        # Create place to stash the quantity data on the instance;
        self._quantity_data: 'QuantityData' = QuantityData(
            quantity_in_g=None,
            pref_unit='g'
        )

        # Now configure the superclass to use this as the data source;
        super().__init__(quantity_data_src=lambda: self._quantity_data, **kwargs)

        if quantity_data is not None:
            self.load_data(quantity_data)

    def _reset_pref_unit(self) -> None:
        """Resets the pref unit"""
        self._quantity_data['pref_unit'] = 'g'

    def _sanitise_pref_unit(self) -> None:
        """Tries to validate the pref unit, and if not valid/not configured, it is reset to 'g'"""
        try:
            _ = self._validate_pref_unit(self._quantity_data['pref_unit'])
        except (
                model.quantity.exceptions.UnknownUnitError,
                model.quantity.exceptions.UnitNotConfiguredError
        ):
            self._reset_pref_unit()

    def set_quantity(self, quantity: float, unit: str) -> None:
        """Sets the quantity in arbitrary units."""
        # Check a non-none value is OK;
        quantity = model.quantity.validation.validate_quantity(quantity)
        # Check the unit is OK;
        unit = self._validate_pref_unit(unit)

        # Calculate the qty in grams;
        g_per_ml = None
        piece_mass_g = None
        if isinstance(self.subject, model.quantity.SupportsExtendedUnits):
            g_per_ml = self.subject.g_per_ml if self.subject.density_is_defined else None
            piece_mass_g = self.subject.piece_mass_g if self.subject.piece_mass_defined else None

        qty_in_g = model.quantity.convert_qty_unit(
            qty=quantity,
            start_unit=unit,
            end_unit='g',
            g_per_ml=g_per_ml,
            piece_mass_g=piece_mass_g
        )

        # OK, go ahead and set;
        self._quantity_data['quantity_in_g'] = qty_in_g
        self._quantity_data['pref_unit'] = unit

    def unset_quantity(self) -> None:
        """Unsets the quantity."""
        self._quantity_data['quantity_in_g'] = None

    def load_data(self, data: 'QuantityData') -> None:
        # Make sure the unit is actually available on this subject;
        data['pref_unit'] = self._validate_pref_unit(data['pref_unit'])
        self._quantity_data = data
