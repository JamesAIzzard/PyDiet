"""Implements functionality associated with modelling one substance as a ratio of another."""
import abc
from typing import Dict, Any

import model
import persistence


class IsQuantityRatioBase(persistence.YieldsPersistableData, abc.ABC):
    """Class to model a ratio between two quantity objects."""

    @property
    @abc.abstractmethod
    def ratio_subject_qty(self) -> 'model.quantity.IsBaseQuantityOf':
        """Returns the quantity instance representing the top of the fraction."""
        raise NotImplementedError

    @property
    def ratio_host_qty(self) -> 'model.quantity.IsBaseQuantityOf':
        """Returns the quantity instance representing the bottom of the fraction."""
        raise NotImplementedError

    @property
    def subject_g_per_host_g(self) -> float:
        """Returns the number of grams of numerator present in every gram of denominator."""
        return self.ratio_subject_qty.quantity_in_g / self.ratio_host_qty.quantity_in_g

    @property
    def subject_qty_in_pref_unit_per_g_of_host(self) -> float:
        """Returns the subject quantity found in a single gram of the host."""
        return model.quantity.convert_qty_unit(
            qty=self.subject_g_per_host_g,
            start_unit='g',
            end_unit=self.ratio_subject_qty.qty_pref_unit
        )

    @property
    def subject_qty_in_pref_unit_per_ref_qty_of_denominator(self) -> float:
        """Returns the numerator mass (in its pref unit) found in every ref quantity of the denominator."""
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
