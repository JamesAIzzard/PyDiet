"""Implements functionality associated with modelling one substance as a ratio of another."""
import abc

import model
import persistence


class HasReadableRatioOf(persistence.YieldsPersistableData, abc.ABC):
    """Base class for all RatioOf classes."""

    @property
    @abc.abstractmethod
    def numerator(self) -> 'model.quantity.HasReadableQuantityOf':
        """Returns the numerator."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def denominator(self) -> 'model.quantity.HasReadableQuantityOf':
        """Returns the denominator"""
        raise NotImplementedError

    @property
    def numerator_g_per_denominator_g(self) -> float:
        """Returns the number of grams of numerator present in every gram of denominator."""
        return self.numerator.quantity_in_g / self.denominator.quantity_in_g

    @property
    def numerator_mass_in_pref_unit_per_g_of_denominator(self) -> float:
        """Returns the numerator mass (in its pref unit) found in every gram of denominator."""
        return model.quantity.convert_qty_unit(
            qty=self.numerator_g_per_denominator_g,
            start_unit='g',
            end_unit=self.numerator.qty_pref_unit
        )

    @property
    def numerator_mass_in_pref_unit_per_ref_qty_of_denominator(self) -> float:
        """Returns the numerator mass (in its pref unit) found in every ref quantity of the denominator."""
        return self.numerator_mass_in_pref_unit_per_g_of_denominator * self.denominator.quantity_in_g

    @property
    def ratio_is_defined(self) -> bool:
        """Returns True/False to indicate if the ratio is defined."""
        return self.numerator.quantity_is_defined and self.denominator.quantity_is_defined

    @property
    def persistable_data(self) -> 'model.quantity.RatioData':
        """Returns the persistable data for the ratio instance."""
        return model.quantity.RatioData(
            numerator_qty_data=self.numerator.persistable_data,
            denominator_qty_data=self.denominator.persistable_data
        )
