"""Defines functionality associated with quantities of substances."""
import abc
from typing import Optional, Any, Callable

import model
import persistence


class HasReadableQuantityOf(persistence.YieldsPersistableData, abc.ABC):
    """Abstract base class to readonly and writable quantities of substances."""
    def __init__(self, qty_subject: Any, **kwargs):
        super().__init__(**kwargs)

        # Subject is *always* stored locally on all subclasses, so stash here;
        self._qty_subject = qty_subject

    @property
    def qty_subject(self) -> Any:
        """Returns the subject whos quantity is being described."""
        return self._qty_subject

    @property
    @abc.abstractmethod
    def _quantity_in_g(self) -> Optional[float]:
        """Returns the object's quantity in grams if defined, otherwise None."""
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
    @abc.abstractmethod
    def _unvalidated_qty_pref_unit(self) -> str:
        """Reterns the preferred unit for referencing the object's quantity."""
        raise NotImplementedError

    @property
    def qty_pref_unit(self) -> str:
        """Returns the unit used to define the subject quantity."""
        # Return the validated unit
        return model.quantity.validation.validate_pref_unit(
            unit=self._unvalidated_qty_pref_unit,
            subject=self.qty_subject
        )

    @property
    def ref_qty(self) -> float:
        """Returns the reference quantity used to define the subject quantity."""
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

    @property
    def persistable_data(self) -> 'model.quantity.QuantityData':
        """Returns the quantity data in the persistable format."""
        # Validate the unit before returning the data;
        _ = model.quantity.validation.validate_pref_unit(
            unit=self.qty_pref_unit,
            subject=self.qty_subject
        )

        # Construct the data object and return it;
        return model.quantity.QuantityData(
            quantity_in_g=self._quantity_in_g,
            pref_unit=self.qty_pref_unit
        )


class HasReadonlyQuantityOf(HasReadableQuantityOf):
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

    @property
    def _quantity_in_g(self) -> Optional[float]:
        """Returns the raw quantity in grams from the source function."""
        return self._quantity_data_src()['quantity_in_g']

    @property
    def _unvalidated_qty_pref_unit(self) -> str:
        """Returns the raw pref unit from the src function."""
        return self._quantity_data_src()['pref_unit']


class HasSettableQuantityOf(HasReadableQuantityOf, persistence.CanLoadData):
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

    def set_quantity(self, quantity: Optional[float], unit: str) -> None:
        """Sets the quantity in arbitrary units."""

        # If quantity is None, just set it right away and break out;
        if quantity is None:
            self._quantity_data['quantity_in_g'] = None
            self._quantity_data['pref_unit'] = 'g'
            return

        # Otherwise, validate it;
        else:
            quantity = model.quantity.validation.validate_quantity(quantity)

        # Check the unit is OK;
        unit = model.quantity.validation.validate_pref_unit(
            unit=unit,
            subject=self.qty_subject
        )

        # Calculate the qty in grams;
        g_per_ml = None
        piece_mass_g = None
        if isinstance(self.qty_subject, model.quantity.HasReadableExtendedUnits):
            g_per_ml = self.qty_subject.g_per_ml if self.qty_subject.density_is_defined else None
            piece_mass_g = self.qty_subject.piece_mass_g if self.qty_subject.piece_mass_is_defined else None

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
