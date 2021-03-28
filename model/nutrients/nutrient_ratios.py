import abc
from typing import Dict, List

from . import configs, exceptions

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
        self._nutrient: 'nutrients.Nutrient' = nutrients.global_nutrients[nutrient_name]
        self._g_per_subject_g: Optional[float] = g_per_subject_g
        self._pref_unit: str = pref_unit

    @property
    def nutrient(self) -> 'nutrients.Nutrient':
        """Returns the nutrient associated with the nutrient ratio."""
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


class HasNutrientRatios(quantity.HasBulk, abc.ABC):
    """Abstract class to model objects with readonly nutrient ratios."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abc.abstractmethod
    def get_nutrient_ratio(self, nutrient_name: str) -> 'NutrientRatio':
        """Returns a NutrientRatio by name."""
        raise NotImplementedError

    @property
    def nutrient_ratios(self) -> Dict[str, 'NutrientRatio']:
        """Returns all nutrient ratios (defined & undefined) by their primary names."""
        nutrient_ratios = {}
        for nutrient_name in configs.all_primary_nutrient_names:
            nutrient_ratios[nutrient_name] = self.get_nutrient_ratio(nutrient_name)
        return nutrient_ratios

    def nutrient_ratio_is_defined(self, nutrient_name: str) -> bool:
        """Returns True/False to indiciate if the named nutrient ratio has been defined."""
        nutrient_name = nutrients.validation.validate_nutrient_name(nutrient_name)
        return self.get_nutrient_ratio(nutrient_name).defined

    @property
    def undefined_mandatory_nutrient_ratios(self) -> List[str]:
        """Returns a list of the mandatory nutrient ratios which are undefined."""
        undefined_mandatory = []
        for nutrient_name in nutrients.configs.mandatory_nutrient_names:
            if not self.nutrient_ratio_is_defined(nutrient_name):
                undefined_mandatory.append(nutrient_name)
        return undefined_mandatory

    @property
    def defined_optional_nutrient_ratios(self) -> List[str]:
        """Returns a list of the optional nutrient names which have been defined."""
        defined_optionals = []
        for nutrient_name, nutrient_ratio in self.nutrient_ratios.items():
            if nutrient_name not in nutrients.configs.mandatory_nutrient_names and nutrient_ratio.defined:
                defined_optionals.append(nutrient_name)
        return defined_optionals

    def _validate_nutrient_ratios(self) -> None:
        """Raises a NutrientRatioGroupError if the set of nutrient ratios are mutually inconsistent."""
        # Check no nutrient group parent weigh's less than its children;
        for parent_nutrient_name in configs.nutrient_group_definitions:
            parent_nutrient_ratio = self.get_nutrient_ratio(parent_nutrient_name)
            if parent_nutrient_ratio.defined:
                child_rolling_total = 0
                for child_nutrient_name in configs.nutrient_group_definitions[parent_nutrient_name]:
                    child_nutrient_ratio = self.get_nutrient_ratio(child_nutrient_name)
                    if child_nutrient_ratio.defined:
                        child_rolling_total = child_rolling_total + child_nutrient_ratio.g_per_subject_g
                if child_rolling_total > parent_nutrient_ratio.g_per_subject_g * 1.01:  # 0.01 to avoid rounding issues.
                    raise nutrients.exceptions.ChildNutrientQtyExceedsParentNutrientQtyError(
                        'The qty of child nutrients of {} exceed its own mass'.format(parent_nutrient_name))


class HasSettableNutrientRatios(HasNutrientRatios, abc.ABC):
    """Abstract class to model objects with settable nutrient ratios."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_nutrient_ratio(self, nutrient_name: str) -> 'SettableNutrientRatio':
        """Gets a settable nutrient ratio instance by name."""
        nutrient_ratio = super().get_nutrient_ratio(nutrient_name)
        if not isinstance(nutrient_ratio, SettableNutrientRatio):
            raise TypeError('Expecting a settable nutrient ratio.')
        return nutrient_ratio

    def set_nutrient_ratios(self, nutrient_ratios_data: Dict[str, 'NutrientRatioData']) -> None:
        """Sets a batch of nutrient ratios from a dictionary of nutrient ratio data."""
        for nutr_name, nr_data in nutrient_ratios_data:
            self.set_nutrient_ratio(
                nutrient_name=nutr_name,
                nutrient_qty=nr_data['nutrient_g_per_subject_g'],
                nutrient_qty_unit='g',
                subject_qty=1,
                subject_qty_unit='g'
            )
            self.set_nutrient_pref_unit(nutrient_name=nutr_name, pref_unit=nr_data['nutrient_pref_units'])

    def set_nutrient_ratio(self, nutrient_name: str,
                           nutrient_qty: Optional[float],
                           nutrient_qty_unit: str,
                           subject_qty: float,
                           subject_qty_unit: str) -> None:
        """Sets the data on a nutrient ratio by name."""
        # Grab the nutrient ratio instance by name;
        nutrient_name = nutrients.get_nutrient_primary_name(nutrient_name)
        nutrient_ratio = self.get_nutrient_ratio(nutrient_name)

        # Take a backup in case we need to revert;
        backup_g_per_subject_g = nutrient_ratio.g_per_subject_g

        # If we are setting to None:
        if nutrient_qty is None:
            nutrient_ratio.g_per_subject_g = None
        # If we are setting to zero;
        elif nutrient_qty == 0:
            nutrient_ratio.g_per_subject_g = 0
        # If we are setting to a non-zero value;
        elif nutrient_qty > 0:
            # Convert the nutrient units into grams;
            if nutrient_qty_unit not in quantity.get_recognised_mass_units():
                raise quantity.exceptions.IncorrectUnitTypeError("Nutrient quantity must be a mass.")
            nutrient_qty_g = quantity.convert_qty_unit(qty=nutrient_qty,
                                                       start_unit=nutrient_qty_unit,
                                                       end_unit='g')

            # Convert the subject units into grams;
            try:
                subject_qty_g = quantity.convert_qty_unit(qty=subject_qty,
                                                          start_unit=subject_qty_unit,
                                                          end_unit='g',
                                                          g_per_ml=self.g_per_ml,
                                                          piece_mass_g=self.piece_mass_g)
            except ValueError:
                if quantity.units_are_volumes(subject_qty_unit):
                    raise quantity.exceptions.DensityNotConfiguredError
                elif quantity.units_are_pieces(subject_qty_unit):
                    raise quantity.exceptions.PcMassNotConfiguredError
                return

            # Check the nutrient qty doesn't exceed the subject qty;
            if nutrient_qty_g > subject_qty_g * 1.001:  # To prevent issues with rounding errors;
                raise nutrients.exceptions.NutrientQtyExceedsSubjectQtyError

            # Calculate the new nutrient ratio;
            new_g_per_subject_g = nutrient_qty_g / subject_qty_g

            # Go ahead and make the change;
            nutrient_ratio.g_per_subject_g = new_g_per_subject_g

        # Now try and validate the changes;
        try:
            self._validate_nutrient_ratios()
        except exceptions.NutrientRatioGroupError as err:
            nutrient_ratio.g_per_subject_g = backup_g_per_subject_g
            raise err

    def zero_nutrient_ratio(self, nutrient_name: str) -> None:
        """Sets the named nutrient ratio to zero."""
        self.set_nutrient_ratio(
            nutrient_name=nutrient_name,
            nutrient_qty=0,
            nutrient_qty_unit='g',
            subject_qty=100,
            subject_qty_unit='g'
        )

    def undefine_nutrient_ratio(self, nutrient_name: str) -> None:
        """Sets the named nutrient ratio to None."""
        self.set_nutrient_ratio(
            nutrient_name=nutrient_name,
            nutrient_qty=None,
            nutrient_qty_unit='g',
            subject_qty=100,
            subject_qty_unit='g'
        )

    def set_nutrient_pref_unit(self, nutrient_name: str, pref_unit: str) -> None:
        """Sets the pref unit for the nutrient ratio."""
        nutrient_ratio = self.get_nutrient_ratio(nutrient_name)
        nutrient_ratio.pref_unit = pref_unit
