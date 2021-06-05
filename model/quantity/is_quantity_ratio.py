"""Implements functionality associated with classes modelling a quantity of one substance as a ratio of a
quantity of another substance."""
import abc
from typing import Dict, Any

import model
import persistence


class IsQuantityRatioOfBase(persistence.YieldsPersistableData, abc.ABC):
    """Base class implementing functionality to model a ratio of two quantities of substance."""

    def __init__(
            self,
            subject_qty: 'model.quantity.IsQuantityOfBase',
            host_qty: 'model.quantity.IsQuantityOfBase'
    ):
        self._ratio_subject_qty = subject_qty
        self._ratio_host_qty = host_qty

    @property
    def ratio_subject_qty(self) -> 'model.quantity.IsQuantityOfBase':
        """Returns the quantity instance representing the top of the fraction."""
        return self._ratio_subject_qty

    @property
    def ratio_host_qty(self) -> 'model.quantity.IsQuantityOfBase':
        """Returns the quantity instance representing the bottom of the fraction."""
        return self._ratio_host_qty

    @property
    def subject_g_per_host_g(self) -> float:
        """Returns the number of grams of the subject present in every gram of the host.
        Example:
            If the subject qty_in_g is 100, and the host qty_in_g is 200, this method
            would return 0.5.
        """
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

    @property
    def persistable_data(self) -> Dict[str, Any]:
        """Returns the persistable data for the quantity ratio."""
        return model.quantity.QuantityRatioData(
            subject_qty_data=self.ratio_subject_qty.persistable_data,
            host_qty_data=self.ratio_host_qty.persistable_data
        )


class IsReadonlyQuantityRatioOf(IsQuantityRatioOfBase):
    """Implements readonly quantity ratio functionality."""

    def __init__(self, **kwargs):

        # Check that we have been given readonly qty instances;
        assert (isinstance(kwargs['subject_qty'], model.quantity.IsReadonlyQuantityOf))
        assert (isinstance(kwargs['host_qty'], model.quantity.IsReadonlyQuantityOf))

        super().__init__(**kwargs)


class IsSettableQuantityRatioOf(IsQuantityRatioOfBase):
    """Impelements settable quantity ratio functionality."""

    def __init__(self, **kwargs):

        # Check that we have been given readonly qty instances;
        assert (isinstance(kwargs['subject_qty'], model.quantity.IsSettableQuantityOf))
        assert (isinstance(kwargs['host_qty'], model.quantity.IsSettableQuantityOf))

        super().__init__(**kwargs)

