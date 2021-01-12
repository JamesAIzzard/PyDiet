from typing import Optional, TYPE_CHECKING

from pydiet import nutrients, quantity, flags
from pydiet.nutrients import exceptions

if TYPE_CHECKING:
    from pydiet.nutrients import Nutrient


class NutrientRatio:
    """Models an amount of nutrient per substance."""

    def __init__(self, nutrient_name: str, g_per_subject_g: Optional[float] = None, pref_unit: str = 'g', **kwds):
        super().__init__(**kwds)
        nutrient_name = nutrients.get_nutrient_primary_name(nutrient_name)
        self._nutrient: 'Nutrient' = nutrients.global_nutrients[nutrient_name]
        self._g_per_subject_g: Optional[float] = g_per_subject_g
        self._pref_unit: str = pref_unit

    @property
    def nutrient(self) -> 'Nutrient':
        return self._nutrient

    @property
    def g_per_subject_g(self) -> Optional[float]:
        """Returns the grams of the nutrient per gram of subject."""
        return self._g_per_subject_g

    def _set_g_per_subject_g(self, g_per_subject_g: Optional[float]) -> None:
        """Implementation for setting g_per_subject_g"""
        raise exceptions.NutrientRatioNotSettableError

    @g_per_subject_g.setter
    def g_per_subject_g(self, g_per_subject_g: Optional[float]) -> None:
        """Sets the number of grams of nutrient per gram of subject."""
        self._set_g_per_subject_g(g_per_subject_g)

    @property
    def pref_unit(self) -> str:
        """Returns the preferred unit used to refer to the nutrient quantity on this instance."""
        return self._pref_unit

    def _set_pref_unit(self, pref_mass_unit: str) -> None:
        """Implementation for setting the pref_unit."""
        raise exceptions.NutrientRatioNotSettableError

    @pref_unit.setter
    def pref_unit(self, pref_mass_unit: str) -> None:
        """Sets the unit used to refer to this nutrient quantity."""
        self._set_pref_unit(pref_mass_unit)

    @property
    def defined(self) -> bool:
        """Returns True/False to indicate if the nutrient ratio is fully defined."""
        return self._g_per_subject_g is not None and self._pref_unit is not None

    @property
    def is_zero(self) -> bool:
        """Returns True/False to indicate if the nutrient ratio is explicitly set to zero."""
        return self._g_per_subject_g == 0

    @property
    def is_non_zero(self) -> bool:
        """Returns True/False to indicate if the nutrient ratio is not zero."""
        return not self.is_zero

    @property
    def summary(self, subject_ref_qty: Optional[float] = None, subject_pref_unit: Optional[float] = None) -> str:
        """Returns a readable summary of the nutrient ratio."""
        template = '{name}: {summary}'
        if not self.defined:
            summary = 'Undefined'
        else:
            nutr_ref_qty = quantity.convert_qty_unit(
                qty=self._g_per_subject_g,
                start_unit='g',
                end_unit=self._pref_unit
            )
            # If subject data was passed, do more detailed summary;
            if subject_pref_unit is not None and subject_ref_qty is not None:
                summary = '{nutr_ref_qty:.3f}{nutr_pref_unit} per {subj_ref_qty}{subj_pref_unit}'.format(
                    nutr_ref_qty=nutr_ref_qty,
                    nutr_pref_unit=self._pref_unit,
                    subj_ref_qty=subject_ref_qty,
                    subj_pref_unit=subject_pref_unit
                )
            else:  # Otherwise just do the basic one;
                summary = '{nutr_ref_qty}{nutr_pref_unit} per g'.format(
                    nutr_ref_qty=nutr_ref_qty,
                    nutr_pref_unit=self._pref_unit
                )
        return template.format(name=self._nutrient.primary_name.replace('_', ' '), summary=summary)


class SettableNutrientRatio(NutrientRatio):
    def __init__(self, **kwds):
        super().__init__(**kwds)

        # Check that we don't have readonly flag_data (this would allow inconsistencies);
        if not isinstance(self, flags.HasSettableFlags):
            assert not isinstance(self, flags.HasFlags)

    def _set_g_per_subject_g(self, g_per_subject_g: Optional[float]) -> None:
        """Implementation for setting grams of nutrient per gram of subject.
        Note:
            This method is not responsible for mutual validation of the set of nutrient ratios
            which may be on the instance. Their mutual validity must be maintained by the instance
            on which they exist.
        """
        if g_per_subject_g is not None:
            self._g_per_subject_g = quantity.validation.validate_quantity(g_per_subject_g)
        else:
            self._g_per_subject_g = None

    def _set_pref_unit(self, pref_mass_unit: str) -> None:
        """Impelmetnation for setting the pref_unit."""
        self._pref_unit = quantity.validation.validate_mass_unit(pref_mass_unit)

    def undefine(self) -> None:
        """Resets g_per_subject_g to None and pref_unit to 'g'."""
        self._g_per_subject_g = None
        self._pref_unit = 'g'
