from typing import Optional, TypedDict

from model import nutrients, quantity, flags


class NutrientRatioData(TypedDict):
    """Persisted data format for NutrientRatio instances."""
    nutrient_g_per_subject_g: Optional[float]
    nutrient_pref_units: str


class NutrientRatio:
    """Models an amount of nutrient per substance."""

    def __init__(self, nutrient_name: str, g_per_subject_g: Optional[float] = None,
                 pref_unit: str = 'g'):
        nutrient_name = nutrients.get_nutrient_primary_name(nutrient_name)
        self._nutrient: nutrients.Nutrient = nutrients.global_nutrients[nutrient_name]
        self._g_per_subject_g: Optional[float] = g_per_subject_g
        self._pref_unit: str = pref_unit

    @property
    def nutrient(self) -> nutrients.Nutrient:
        return self._nutrient

    @property
    def g_per_subject_g(self) -> Optional[float]:
        """Returns the grams of the nutrient per gram of subject."""
        return self._g_per_subject_g

    @property
    def pref_unit(self) -> str:
        """Returns the preferred unit used to refer to the nutrient quantity on this instance."""
        return self._pref_unit

    @property
    def defined(self) -> bool:
        """Returns True/False to indicate if the nutrient ratio is fully defined."""
        return self._g_per_subject_g is not None and self._pref_unit is not None

    @property
    def undefined(self) -> bool:
        """Returns True/False to inidcate if the nutrient ratio is undefined."""
        return not self.defined

    @property
    def is_zero(self) -> bool:
        """Returns True/False to indicate if the nutrient ratio is explicitly set to zero."""
        return self._g_per_subject_g == 0

    @property
    def is_non_zero(self) -> bool:
        """Returns True/False to indicate if the nutrient ratio is not zero."""
        return not self.is_zero


class SettableNutrientRatio(NutrientRatio):

    def __init__(self, nutrient_name: str, g_per_subject_g: Optional[float] = None,
                 pref_unit: str = 'g'):
        # Check that we don't have readonly flag_data (this would allow inconsistencies);
        if not isinstance(self, flags.HasSettableFlags):
            assert not isinstance(self, flags.HasFlags)
        super().__init__(nutrient_name, g_per_subject_g, pref_unit)

    @NutrientRatio.g_per_subject_g.setter
    def g_per_subject_g(self, g_per_subject_g: Optional[float]) -> None:
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

    @NutrientRatio.pref_unit.setter
    def pref_unit(self, pref_mass_unit: str) -> None:
        """Impelmetnation for setting the pref_unit."""
        self._pref_unit = quantity.validation.validate_mass_unit(pref_mass_unit)

    def undefine(self) -> None:
        """Resets g_per_subject_g to None and pref_unit to 'g'."""
        self._g_per_subject_g = None
        self._pref_unit = 'g'

    def zero(self) -> None:
        """Zeroes the nutrient ratio."""
        self._g_per_subject_g = 0
