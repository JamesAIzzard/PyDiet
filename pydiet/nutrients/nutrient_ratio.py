from typing import Dict, Optional, TYPE_CHECKING

from pydiet import nutrients, quantity, flags
from pydiet.nutrients import exceptions

if TYPE_CHECKING:
    from pydiet.nutrients import HasNutrientRatios, Nutrient


class NutrientRatio:
    """Models an amount of nutrient per substance."""

    def __init__(self, nutrient_name: str, subject: 'HasNutrientRatios', g_per_subject_g: Optional[float] = None,
                 pref_unit: str = 'g', **kwds):
        super().__init__(**kwds)
        nutrient_name = nutrients.get_nutrient_primary_name(nutrient_name)
        self._nutrient: 'Nutrient' = nutrients.global_nutrients[nutrient_name]
        self._g_per_subject_g: Optional[float] = g_per_subject_g
        self._pref_unit: str = pref_unit
        self._children: Dict[str, 'NutrientRatio']
        self._parent: Dict[str, 'NutrientRatio']
        self._subject: 'HasNutrientRatios' = subject

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
    def summary(self) -> str:
        """Returns a readable summary of the nutrient ratio."""
        template = '{name}: {summary}'
        defined_template = '{nutr_qty:.3f}{nutr_unit} per {subj_qty}{subj_unit}'
        if not self.defined:
            summary = 'Undefined'
        else:
            nutr_ref_qty_g = self._g_per_subject_g * self._subject.ref_qty_in_g
            nutr_ref_qty = quantity.convert_qty_unit(qty=nutr_ref_qty_g,
                                                     start_unit='g',
                                                     end_unit=self._pref_unit)
            summary = defined_template.format(
                nutr_qty=nutr_ref_qty,
                nutr_unit=self._pref_unit,
                subj_qty=self._subject.ref_qty,
                subj_unit=self._subject.pref_unit
            )
        return template.format(name=self._nutrient.primary_name.replace('_', ' '), summary=summary)


class SettableNutrientRatio(NutrientRatio):
    def __init__(self, **kwds):
        super().__init__(**kwds)

        # Check that we don't have readonly flags (this would allow inconsistencies);
        if not isinstance(self, flags.HasSettableFlags):
            assert not isinstance(self, flags.HasFlags)

    def _set_g_per_subject_g(self, g_per_subject_g: Optional[float]) -> None:
        """Implementation for setting grams of nutrient per gram of subject."""
        # Backup the g_per_subject_g value in case validation fails;
        g_per_subject_g_backup = self._g_per_subject_g
        # Set the new one and validate;
        self._g_per_subject_g = g_per_subject_g
        try:
            self._validate()
        except exceptions.InvalidNutrientQtyError as err:
            self._g_per_subject_g = g_per_subject_g_backup
            raise err

        # Update any related flags if instance is equipped;
        if isinstance(self, flags.HasSettableFlags):
            ...

    def _set_pref_unit(self, pref_mass_unit: str) -> None:
        """Impelmetnation for setting the pref_unit."""
        self._pref_unit = quantity.validation.validate_mass_unit(pref_mass_unit)

    def undefine(self) -> None:
        """Resets g_per_subject_g to None and pref_unit to 'g'."""
        self._g_per_subject_g = None
        self._pref_unit = 'g'

    def _validate(self) -> None:
        """Validates the g_per_subject_g in the context of parent and child nutrient ratios."""
        # Todo
