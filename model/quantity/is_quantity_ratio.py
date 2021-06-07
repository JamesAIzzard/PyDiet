"""Implements functionality associated with classes modelling a quantity of one substance as a ratio of a
quantity of another substance."""
import abc
from typing import Dict, Callable, Optional, Any

import model
import persistence


class IsQuantityRatioBase(persistence.YieldsPersistableData, abc.ABC):
    """Base class implementing functionality to model a ratio of two quantities of substance."""

    def __init__(self, ratio_subject: Any, ratio_host: Any, **kwargs):

        super().__init__(**kwargs)

        # Stash the ratio quantities;
        self._ratio_subject = ratio_subject
        self._ratio_host = ratio_host

    @property
    @abc.abstractmethod
    def quantity_ratio_data(self) -> 'model.quantity.QuantityRatioData':
        """Returns the data for the quantity ratio."""
        raise NotImplementedError

    @property
    def ratio_subject_qty(self) -> 'model.quantity.IsReadonlyQuantityOf':
        """Returns the quantity instance representing the top of the fraction."""
        return model.quantity.IsReadonlyQuantityOf(
            qty_subject=self._ratio_subject,
            quantity_data_src=lambda: self.quantity_ratio_data['subject_qty_data']
        )

    @property
    def ratio_host_qty(self) -> 'model.quantity.IsReadonlyQuantityOf':
        """Returns the quantity instance representing the bottom of the fraction."""
        return model.quantity.IsReadonlyQuantityOf(
            qty_subject=self._ratio_host,
            quantity_data_src=lambda: self.quantity_ratio_data['host_qty_data']
        )

    @property
    def subject_g_per_host_g(self) -> float:
        """Returns the number of grams of the subject present in every gram of the host.
        Example:
            If the subject qty_in_g is 100, and the host qty_in_g is 200, this method
            would return 0.5.
        """
        # Raise an exception if we are not defined;
        if not self.ratio_is_defined:
            raise model.nutrients.exceptions.UndefinedNutrientRatioError(
                subject=self
            )

        # Otherwise, crack on;
        return self.ratio_subject_qty.quantity_in_g / self.ratio_host_qty.quantity_in_g

    @property
    def subject_qty_in_pref_unit_per_g_of_host(self) -> float:
        """Returns the subject quantity (in its pref unit) found in a single gram of the host.
        Example:
            If the subject pref_unit was 'kg', this property would return the number of kg we
            would find in every gram of the host.
        """
        return model.quantity.convert_qty_unit(
            qty=self.subject_g_per_host_g,
            start_unit='g',
            end_unit=self.ratio_subject_qty.qty_pref_unit
        )

    @property
    def subject_qty_in_pref_unit_per_ref_qty_of_host(self) -> float:
        """Returns the subject quantity in its pref unit, found in each reference quantity of the host.
        Example:
            If the subject has pref units mg, and the host has a reference quantity of
            2kg, this method will return the number of milligrams found in every 2kg of the subject.
        """
        return self.subject_qty_in_pref_unit_per_g_of_host * self.ratio_host_qty.quantity_in_g

    @property
    def ratio_is_defined(self) -> bool:
        """Returns True/False to indicate if the ratio is defined."""
        return self.ratio_subject_qty.quantity_is_defined and self.ratio_host_qty.quantity_is_defined

    @property
    def ratio_is_zero(self) -> bool:
        """Returns True/False to indicate if the numerator qty is zero."""
        return self.subject_g_per_host_g == 0

    def validate_quantity_ratio(self) -> None:
        """Checks the ratio is valid."""
        # If the ratio isn't defined, don't worry;
        if not self.ratio_is_defined:
            return

        # Dissallow zero host qty, this obviously breaks the universe;
        if self.ratio_host_qty.quantity_in_g == 0:
            raise model.quantity.exceptions.ZeroQuantityRatioHostError(
                subject=self
            )

        # Check the nutrient qty doesn't exceed the subject qty;
        if self.ratio_subject_qty.quantity_in_g > self.ratio_host_qty.quantity_in_g:
            raise model.quantity.exceptions.SubjectQtyExceedsHostQtyError(
                subject=self
            )

    @property
    def persistable_data(self) -> Dict[str, Any]:
        """Returns the persistable data for the quantity ratio."""

        return model.quantity.QuantityRatioData(
            subject_qty_data=self.ratio_subject_qty.persistable_data,
            host_qty_data=self.ratio_host_qty.persistable_data
        )


class IsReadonlyQuantityRatio(IsQuantityRatioBase):
    """Models a readonly quantity ratio."""

    def __init__(self, qty_ratio_data_src: Callable[[], 'model.quantity.QuantityRatioData'], **kwargs):
        super().__init__(**kwargs)

        # Stash the data src;
        self._qty_ratio_data_src = qty_ratio_data_src

        # Validate the data;
        self.validate_quantity_ratio()

    @property
    def quantity_ratio_data(self) -> 'model.quantity.QuantityRatioData':
        """Returns the qty ratio data."""
        return self._qty_ratio_data_src()


class IsSettableQuantityRatio(IsQuantityRatioBase, persistence.CanLoadData):
    """Models a settable quantity ratio."""

    def __init__(self, qty_ratio_data: Optional['model.quantity.QuantityRatioData'] = None, **kwargs):
        super().__init__(**kwargs)

        # Create two settable qty instances locally;
        self._ratio_subject_qty = model.quantity.IsSettableQuantityOf(
            qty_subject=kwargs['ratio_subject'],
            quantity_data=model.quantity.QuantityData(
                quantity_in_g=None,
                pref_unit='g'
            )
        )
        self._ratio_host_qty = model.quantity.IsSettableQuantityOf(
            qty_subject=kwargs['ratio_host'],
            quantity_data=model.quantity.QuantityData(
                quantity_in_g=None,
                pref_unit='g'
            )
        )

        if qty_ratio_data is not None:
            self.load_data(qty_ratio_data)

    @property
    def quantity_ratio_data(self) -> 'model.quantity.QuantityRatioData':
        """Returns the data for the quantity ratio."""
        return model.quantity.QuantityRatioData(
            subject_qty_data=self._ratio_subject_qty.persistable_data,
            host_qty_data=self._ratio_host_qty.persistable_data
        )

    def set_quantity_ratio(
            self,
            subject_quantity_value: Optional[float],
            subject_quantity_unit: str,
            host_quantity_value: Optional[float],
            host_quantity_unit: str
    ) -> None:
        """Sets the quantity ratio using arbitrary units."""

        # If either subject or host is None, go ahead and unset;
        if subject_quantity_value is None:
            self._ratio_subject_qty.unset_quantity()
        if host_quantity_value is None:
            self._ratio_host_qty.unset_quantity()

        # Take a backup in case we fail validation later;
        backup_data = self.persistable_data

        # Go ahead and set;
        self._ratio_subject_qty.set_quantity(
            quantity_value=subject_quantity_value,
            quantity_unit=subject_quantity_unit
        )
        self._ratio_host_qty.set_quantity(
            quantity_value=host_quantity_value,
            quantity_unit=host_quantity_unit
        )

        # Run the validation;
        try:
            self.validate_quantity_ratio()
        except Exception as err:
            self.load_data(backup_data)
            raise err

    def unset_quantity_ratio(self) -> None:
        """Unsets the quantity ratio."""
        self._ratio_subject_qty.unset_quantity()
        self._ratio_host_qty.unset_quantity()

    def zero_quantity_ratio(self):
        """Zeroes the subject of the quantity ratio."""
        self._ratio_subject_qty.set_quantity(quantity_value=0)

    def load_data(self, quantity_ratio_data: 'model.quantity.QuantityRatioData') -> None:
        """Loads data into the instance."""

        # Take a backup of the previous data;
        backup_data = self.persistable_data

        # Load the data;
        self._ratio_subject_qty.load_data(quantity_data=quantity_ratio_data['subject_qty_data'])
        self._ratio_host_qty.load_data(quantity_data=quantity_ratio_data['host_qty_data'])

        # Validate the data;
        try:
            self.validate_quantity_ratio()
        except Exception as err:
            # Something went wrong, put the original data back and pass the exception on.
            self.load_data(backup_data)
            raise err
