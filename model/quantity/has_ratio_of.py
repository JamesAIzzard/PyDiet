"""Implements functionality associated with modelling one substance as a ratio of another."""
import abc

import model


class HasRatioOf:
    """Class to implement ratio functionality."""

    @property
    @abc.abstractmethod
    def _numerator(self) -> 'model.quantity.HasReadableQuantityOf':
        """Returns the numerator."""
        raise NotImplementedError

    @property
    def _denominator(self) -> 'model.quantity.HasReadableQuantityOf':
        """Returns the denominator"""
        raise NotImplementedError

    @property
    def g_per_subject_g(self) -> float:
        """Returns the number of grams of numerator present in every gram of denominator."""
        return self._numerator.quantity_in_g / self._denominator.quantity_in_g

    @property
    def _numerator_mass_in_pref_unit_per_g_of_denominator(self) -> float:
        """Returns the numerator mass (in its pref unit) found in every gram of denominator."""
        return model.quantity.convert_qty_unit(
            qty=self.g_per_subject_g,
            start_unit='g',
            end_unit=self._numerator.qty_pref_unit
        )

    @property
    def _numerator_mass_in_pref_unit_per_ref_qty_of_denominator(self) -> float:
        """Returns the numerator mass (in its pref unit) found in every ref quantity of the denominator."""
        return self._numerator_mass_in_pref_unit_per_g_of_denominator * self._denominator.quantity_in_g

    @property
    def ratio_is_defined(self) -> bool:
        """Returns True/False to indicate if the ratio is defined."""
        return self._numerator.quantity_is_defined and self._denominator.quantity_is_defined

    @property
    def ratio_is_zero(self) -> bool:
        """Returns True/False to indicate if the numerator qty is zero."""
        return self.g_per_subject_g == 0
