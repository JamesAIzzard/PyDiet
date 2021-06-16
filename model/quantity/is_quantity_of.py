"""Implements functionality associated with classes modelling a quantity of a substance."""
import abc
from typing import Optional, Any, Callable

import model
import persistence


class IsQuantityOfBase(persistence.YieldsPersistableData, abc.ABC):
    """Base class implementing functionality to model a quantity of substance."""
    def __init__(self, qty_subject: Any, **kwargs):
        super().__init__(**kwargs)

        # Subject is *always* stored locally on all subclasses, so stash here;
        self._qty_subject = qty_subject

    @property
    @abc.abstractmethod
    def _quantity_in_g(self) -> Optional[float]:
        """Returns the object's quantity in grams if defined, otherwise None."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def _unvalidated_qty_pref_unit(self) -> str:
        """Reterns the preferred unit for referencing the object's quantity."""
        raise NotImplementedError

    @property
    def quantity_in_g(self) -> float:
        """Returns the object's quantity in grams."""
        _qty_in_g = self._quantity_in_g
        if _qty_in_g is None:
            raise model.quantity.exceptions.UndefinedQuantityError()
        else:
            return _qty_in_g

    @property
    def qty_subject(self) -> Any:
        """Returns the subject whos quantity is being described."""
        return self._qty_subject

    @property
    def qty_pref_unit(self) -> str:
        """Returns the unit used to define the subject quantity.
        Example:
            If the qty_in_g is 100, and the pref unit is kg, this property would
            return 0.1, because 100g expressed in into kg is 0.1.
        """
        # Check the instance is valid before returning data;
        self.validate_quantity_and_unit()
        # Return
        return model.quantity.validation.validate_qty_unit(self._unvalidated_qty_pref_unit)

    @property
    def ref_qty(self) -> float:
        """Returns the reference quantity used to define the subject quantity.

        """
        # Check the instance is valid before returning data;
        self.validate_quantity_and_unit()

        # Configure the extended unit variables to match the subject;
        g_per_ml = None
        piece_mass_g = None
        # If we have exended units, place them in if they are set;
        if isinstance(self.qty_subject, model.quantity.HasReadableExtendedUnits):
            g_per_ml = self.qty_subject.g_per_ml if self.qty_subject.density_is_defined else None
            piece_mass_g = self.qty_subject.piece_mass_g if self.qty_subject.piece_mass_is_defined else None

        # Do the conversion and return the result;
        return model.quantity.convert_qty_unit(
            qty=self.quantity_in_g,
            start_unit='g',
            end_unit=self.qty_pref_unit,
            g_per_ml=g_per_ml,
            piece_mass_g=piece_mass_g
        )

    @property
    def quantity_is_defined(self) -> bool:
        """Returns True/False to indicate if the quantity is defined."""
        return self._quantity_in_g is not None

    def validate_quantity_and_unit(self) -> None:
        """Runs validation on the quantity of instance."""

        # Check the quantity value is viable if set;
        if self.quantity_is_defined:
            _ = model.quantity.validation.validate_quantity(self._quantity_in_g)

        # Check the unit is supported;
        _ = model.quantity.validation.validate_pref_unit(
            unit=self._unvalidated_qty_pref_unit,
            subject=self.qty_subject
        )

    @property
    def persistable_data(self) -> 'model.quantity.QuantityData':
        """Returns the quantity data in the persistable format."""

        # Construct the data object and return it;
        return model.quantity.QuantityData(
            quantity_in_g=self._quantity_in_g,
            pref_unit=self.qty_pref_unit
        )


class IsReadonlyQuantityOf(IsQuantityOfBase):
    """Implements functionality associated with a readonly quantity of substance.

    Notes:
        Instances inheriting from QuantityOf do not export the subject's persistable data in
        their persistable data.

        Since this quantity may come from anywhere, it is not stored locally. This class
        may also be instantiated directly, so we can't rely on an abstract class.
        Instead we take advantage of closures and pass in a callback as a data source.
    """

    def __init__(self, quantity_data_src: Callable[[], 'model.quantity.QuantityData'], **kwargs):
        super().__init__(**kwargs)

        # Stash the data source callable;
        self._quantity_data_src = quantity_data_src

        # Validate the src;
        self.validate_quantity_and_unit()

    @property
    def _quantity_in_g(self) -> Optional[float]:
        """Returns the raw quantity in grams from the source function."""
        return self._quantity_data_src()['quantity_in_g']

    @property
    def _unvalidated_qty_pref_unit(self) -> str:
        """Returns the raw pref unit from the src function."""
        return self._quantity_data_src()['pref_unit']


class IsSettableQuantityOf(IsQuantityOfBase, persistence.CanLoadData):
    """Implements functionality associated with a settable quantity of substance."""

    def __init__(self, quantity_data: Optional['model.quantity.QuantityData'] = None, **kwargs):
        super().__init__(**kwargs)

        # Now we are storing the data locally, so create a place to stash the data on the instance;
        self._quantity_data: 'model.quantity.QuantityData' = model.quantity.QuantityData(
            quantity_in_g=None,
            pref_unit='g'
        )

        # If we got quantity data, then load it;
        if quantity_data is not None:
            self.load_data(quantity_data)

    @property
    def _quantity_in_g(self) -> Optional[float]:
        """Returns the locally stored quantity in grams if defined, otherwise None."""
        return self._quantity_data['quantity_in_g']

    @property
    def _unvalidated_qty_pref_unit(self) -> str:
        return self._quantity_data['pref_unit']

    def _reset_qty_pref_unit(self) -> None:
        """Resets the pref unit"""
        self._quantity_data['pref_unit'] = 'g'

    def _sanitise_qty_pref_unit(self) -> None:
        """Tries to validate the pref unit, and if not valid/not configured, it is reset to 'g'"""
        try:
            _ = model.quantity.validation.validate_pref_unit(
                unit=self._unvalidated_qty_pref_unit,
                subject=self.qty_subject
            )
        except (
                model.quantity.exceptions.UnknownUnitError,
                model.quantity.exceptions.UnitNotConfiguredError
        ):
            self._reset_qty_pref_unit()

    def set_quantity(self, quantity_value: Optional[float] = None, quantity_unit: Optional[str] = None) -> None:
        """Sets the quantity in arbitrary units."""

        # If the unit was not specified, just use the existing one;
        if quantity_unit is None:
            quantity_unit = self.qty_pref_unit

        # Catch use of extended units when unsupported by subject;
        if model.quantity.unit_is_extended(quantity_unit) and not isinstance(
                self.qty_subject, model.quantity.HasReadableExtendedUnits
        ):
            raise model.quantity.exceptions.UnsupportedExtendedUnitsError(
                subject=self.qty_subject
            )

        # Validate the unit to correct any case issues;
        quantity_unit = model.quantity.validation.validate_qty_unit(quantity_unit)

        # Validate the quantity value if not None;
        if quantity_value is not None:
            quantity_value = model.quantity.validation.validate_quantity(quantity_value)

        # If the qty value was set, we need to convert it to grams;
        if quantity_value is not None:
            g_per_ml = None
            piece_mass_g = None
            if isinstance(self.qty_subject, model.quantity.HasReadableExtendedUnits):
                g_per_ml = self.qty_subject.g_per_ml if self.qty_subject.density_is_defined else None
                piece_mass_g = self.qty_subject.piece_mass_g if self.qty_subject.piece_mass_is_defined else None

            qty_in_g = model.quantity.convert_qty_unit(
                qty=quantity_value,
                start_unit=quantity_unit,
                end_unit='g',
                g_per_ml=g_per_ml,
                piece_mass_g=piece_mass_g
            )
        # Otherwise, just set it to None;
        else:
            qty_in_g = None

        # Take a backup of the data, in case validation fails;
        backup_data = self.persistable_data

        # OK, go ahead and set;
        self._quantity_data['quantity_in_g'] = qty_in_g
        self._quantity_data['pref_unit'] = quantity_unit

        # OK, run any validation;
        try:
            self.validate_quantity_and_unit()
        # Ahh, OK, something broke, reset the original value and pass the exception on;
        except Exception as err:
            self.load_data(backup_data)
            raise err

    def unset_quantity(self) -> None:
        """Unsets the quantity."""
        self.set_quantity(quantity_value=None)

    def load_data(self, quantity_data: 'model.quantity.QuantityData') -> None:
        """Load the any available data into the instance."""

        # If the pref unit is defined, make sure it is available on this subject;
        if quantity_data['pref_unit'] is not None:
            quantity_data['pref_unit'] = model.quantity.validation.validate_pref_unit(
                unit=quantity_data['pref_unit'],
                subject=self.qty_subject
            )

        # Put the data onto the subject.
        self._quantity_data = quantity_data
