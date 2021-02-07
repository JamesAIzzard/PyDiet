import abc
from typing import Dict, List

from . import validation, configs, exceptions
from model import quantity, nutrients


class HasNutrientRatios(quantity.HasBulk, abc.ABC):
    """Abstract class to model objects with readonly nutrient ratios."""

    def __init__(self, **kwargs):
        """
        HasNutrientRatios constructor.
        Keyword Args:
            nutrient_ratios (Dict[str, NutrientRatio]): NutrientRatio instances
                to be loaded into this object.
        """
        super().__init__(**kwargs)
        self._nutrient_ratios: Dict[str, 'nutrients.NutrientRatio'] = {}
        # Start by populating the list with fresh instances;
        for nutr_name in configs.all_primary_nutrient_names:
            if nutr_name not in self._nutrient_ratios:
                if isinstance(self, HasSettableNutrientRatios):
                    self._nutrient_ratios[nutr_name] = nutrients.SettableNutrientRatio(nutrient_name=nutr_name)
                else:
                    self._nutrient_ratios[nutr_name] = nutrients.NutrientRatio(nutrient_name=nutr_name)
        # Now update list with any data that has been passed in;
        if 'nutrient_ratios' in kwargs.keys():
            # Import any nutrient ratio data supplied;
            for nutr_name, nr in kwargs['nutrient_ratios'].items():
                prim_nutr_name = validation.validate_nutrient_name(nutr_name)
                self._nutrient_ratios[prim_nutr_name] = nr

    def get_nutrient_ratio(self, nutrient_name: str) -> 'nutrients.NutrientRatio':
        """Returns a NutrientRatio by name."""
        nutrient_name = validation.validate_nutrient_name(nutrient_name)
        return self._nutrient_ratios[nutrient_name]

    @property
    def nutrient_ratios(self) -> Dict[str, 'nutrients.NutrientRatio']:
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

    @property
    def nutrient_ratios_data(self) -> Dict[str, nutrients.NutrientRatioData]:
        """Returns a dict of all nutrient names and corresponding NutrientRatioData fields."""
        return {nutr_name: nutrients.NutrientRatioData(
            nutrient_g_per_subject_g=nutr_ratio.g_per_subject_g,
            nutrient_pref_units=nutr_ratio.pref_unit
        ) for nutr_name, nutr_ratio in self._nutrient_ratios.keys()}


class HasSettableNutrientRatios(HasNutrientRatios, abc.ABC):
    """Abstract class to model objects with settable nutrient ratios."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_nutrient_ratios(self, nutrient_ratios_data: Dict[str, nutrients.NutrientRatioData]) -> None:
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
                           nutrient_qty: float,
                           nutrient_qty_unit: str,
                           subject_qty: float,
                           subject_qty_unit: str) -> None:
        """Sets the data on a nutrient ratio by name."""
        # Convert the nutrient units into grams;
        if nutrient_qty_unit not in quantity.get_recognised_mass_units():
            raise quantity.exceptions.IncorrectUnitTypeError("Nutrient quantity must be a mass.")
        nutrient_qty_g = quantity.convert_qty_unit(qty=nutrient_qty,
                                                   start_unit=nutrient_qty_unit,
                                                   end_unit='g')
        # Grab the nutrient ratio instance by name;
        nutrient_name = nutrients.get_nutrient_primary_name(nutrient_name)
        nutrient_ratio = self.get_nutrient_ratio(nutrient_name)
        # Take a backup in case we need to revert;
        backup_g_per_subject_g = nutrient_ratio.g_per_subject_g
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
        # Calculate the new nutrient ratio;
        new_g_per_subject_g = nutrient_qty_g / subject_qty_g
        # Go ahead and make the change;
        nutrient_ratio.g_per_subject_g = new_g_per_subject_g
        # Now try and validate it;
        try:
            self._validate_nutrient_ratios()
        except exceptions.NutrientRatioGroupError as err:
            nutrient_ratio.g_per_subject_g = backup_g_per_subject_g
            raise err

    def set_nutrient_pref_unit(self, nutrient_name: str, pref_unit: str) -> None:
        """Sets the pref unit for the nutrient ratio."""
        nutrient_ratio = self.get_nutrient_ratio(nutrient_name)
        nutrient_ratio.pref_unit = pref_unit
