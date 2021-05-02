from typing import TypedDict, Optional, Any

import model
import persistence


class QuantityData(TypedDict):
    quantity_in_g: Optional[float]
    ref_qty: float
    pref_unit: str


class QuantityOf(model.SupportsDefinition, persistence.CanLoadData):
    """Models a quantity of a substance."""

    def __init__(self, subject: Any, quantity_data: Optional['QuantityData'] = None, **kwargs):
        super().__init__(**kwargs)

        self._subject = subject
        self._quantity_data: 'QuantityData' = QuantityData(
            quantity_in_g=None,
            ref_qty=100,
            pref_unit='g'
        )

        if quantity_data is not None:
            self.load_data(quantity_data)

    def _reset_pref_unit(self) -> None:
        self._quantity_data['pref_unit'] = 'g'
        self._quantity_data['ref_qty'] = 100

    def _sanitise_pref_unit(self) -> None:
        try:
            _ = self._validate_pref_unit(self._quantity_data['pref_unit'])
        except (
                model.quantity.exceptions.UnknownUnitError,
                model.quantity.exceptions.UnitNotConfiguredError
        ):
            self._reset_pref_unit()

    def _validate_pref_unit(self, unit: str) -> str:
        # If the unit isn't recognised, just replace it with grams
        unit = model.quantity.validation.validate_qty_unit(unit)

        # If the subject doesn't support extended units;
        if not isinstance(self._subject, model.quantity.SupportsExtendedUnits):
            # If the unit is a volume, raise the volume exception;
            if model.quantity.units_are_volumes(unit):
                raise model.quantity.exceptions.UndefinedDensityError(subject=self.subject)
            # If the unit is a pc, raise the pc exception;
            if model.quantity.units_are_pieces(unit):
                raise model.quantity.exceptions.UndefinedPcMassError(subject=self.subject)

        # OK, so the subject does support extended units;
        # If the unit is a volume, and the subject doesn't have density defined;
        if model.quantity.units_are_volumes(unit) and not self._subject.density_is_defined:
            raise model.quantity.exceptions.UndefinedDensityError(subject=self.subject)
        elif model.quantity.units_are_pieces(unit) and not self._subject.piece_mass_defined:
            raise model.quantity.exceptions.UndefinedPcMassError(subject=self.subject)

        # OK, return the unit;
        return unit

    @property
    def subject(self) -> Any:
        """Returns the subject whos quantity is being described."""
        return self._subject

    @property
    def quantity_in_g(self) -> float:
        """Returns the object's quantity in grams."""
        if self._quantity_data['quantity_in_g'] is None:
            raise model.quantity.exceptions.UndefinedQuantityError()
        else:
            return self._quantity_data['quantity_in_g']

    @property
    def pref_unit(self) -> str:
        """Returns the unit used to define the subject quantity.
        Notes:
            By sanitising the pref unit, we can stop this class returning
            units that are not configured on the subject.
        """
        self._sanitise_pref_unit()
        return self._quantity_data['pref_unit']

    @property
    def ref_qty(self) -> float:
        """Returns the reference quantity used to define the subject quantity."""
        self._sanitise_pref_unit()
        return self._quantity_data['ref_qty']

    @property
    def is_defined(self) -> bool:
        return self._quantity_data['quantity_in_g'] is not None

    def load_data(self, data: 'QuantityData') -> None:
        self._quantity_data = data

    @property
    def persistable_data(self) -> 'QuantityData':
        return self._quantity_data


class SettableQuantityOf(QuantityOf):
    """Models a settable quantity of substance."""

    def set_quantity(self, quantity: Optional[float], unit: str) -> None:
        """Sets the quantity in arbitrary units."""
        # Set a None value immediately;
        if quantity is None:
            self._quantity_data['quantity_in_g'] = None
        # Check a non-none value is OK;
        else:
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
        self._quantity_data['ref_qty'] = quantity
        self._quantity_data['pref_unit'] = unit
