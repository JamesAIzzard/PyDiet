import abc
from typing import Dict, List, TYPE_CHECKING

import pydiet
from pydiet import nutrients, quantity, flags
from pydiet.nutrients import configs, exceptions
from pydiet.quantity import HasBulk

if TYPE_CHECKING:
    from pydiet.nutrients import NutrientRatio, SettableNutrientRatio


class HasNutrientRatios(HasBulk, abc.ABC):

    def __init__(self, **kwds):
        super().__init__(**kwds)

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

    @property
    def defined_optional_nutrient_names(self) -> List[str]:
        """Returns a list of the optional nutrient names which have been defined."""
        defined_optionals = []
        for nutrient_name, nutrient_ratio in self.nutrient_ratios.items():
            if nutrient_name not in nutrients.configs.mandatory_nutrient_names and nutrient_ratio.defined:
                defined_optionals.append(nutrient_name)
        return defined_optionals

    @property
    def nutrients_summary(self) -> str:
        """Returns a readable summary of all mandatory and additionally defined nutrients."""
        output = ''
        for nutrient_name in configs.mandatory_nutrient_names + self.defined_optional_nutrient_names:
            output = output + '{name:<30} {summary:<30}\n'.format(
                name=nutrient_name.replace('_', ' ') + ':',
                summary=self.get_nutrient_ratio(nutrient_name).summary
            )
        return output


class HasSettableNutrientRatios(HasNutrientRatios, abc.ABC):

    @abc.abstractmethod
    def get_nutrient_ratio(self, nutrient_name: str) -> 'SettableNutrientRatio':
        """Returns a SettableNutrientRatio by name."""
        raise NotImplementedError

    def set_nutrient_ratio(self, nutrient_name: str,
                           nutrient_qty: float,
                           nutrient_qty_unit: str,
                           subject_qty: float,
                           subject_qty_unit: str) -> None:
        """Sets the data on a nutrient ratio by name."""
        # Set the new ratio, or raise exception and revert if invalid;
        nutrient_name = nutrients.get_nutrient_primary_name(nutrient_name)
        nutrient_ratio = self.get_nutrient_ratio(nutrient_name)
        backup_g_per_subject_g = nutrient_ratio.g_per_subject_g
        subject_qty_g = quantity.convert_qty_unit(qty=subject_qty,
                                                  start_unit=subject_qty_unit,
                                                  end_unit='g')
        nutrient_qty_g = quantity.convert_qty_unit(qty=nutrient_qty,
                                                   start_unit=nutrient_qty_unit,
                                                   end_unit='g')
        new_g_per_subject_g = nutrient_qty_g / subject_qty_g
        nutrient_ratio.g_per_subject_g = new_g_per_subject_g
        try:
            self._validate_nutrient_ratios()
        except exceptions.NutrientRatioGroupError as err:
            nutrient_ratio.g_per_subject_g = backup_g_per_subject_g
            raise err

        # Check for defined & conflicting flag_data (hard conflicts);
        if isinstance(self, flags.HasFlags):
            for relation in pydiet.nutrient_flag_relations[nutrient_name]:
                # Raise an exception in any of the four cases (in order of appearance):
                # 1. Flag is True, and implies nutrient should be non-zero, but nutrient is zero.
                # 2. Flag is True, and implies nutrient should be zero, but nutrient is non-zero.
                # 3. Nutrient is non-zero, matching flag, but flag is False.
                # 4. Nutrient is zero, matching flag, but flag is False.
                if self.flag_is_true(relation.flag_name):
                    if relation.implies_has_nutrient and new_g_per_subject_g == 0:  # 1.
                        raise pydiet.exceptions.FlagNutrientConflictError
                    elif relation.implies_has_no_nutrient and new_g_per_subject_g > 0:  # 2.
                        raise pydiet.exceptions.FlagNutrientConflictError
                elif self.flag_is_false(relation.flag_name):
                    if relation.implies_has_nutrient and new_g_per_subject_g > 0:  # 3.
                        raise pydiet.exceptions.FlagNutrientConflictError
                    elif relation.implies_has_no_nutrient and new_g_per_subject_g == 0:  # 4.
                        raise pydiet.exceptions.FlagNutrientConflictError

        # Update any unset and related flag_data (soft conflicts);
        if isinstance(self, flags.HasSettableFlags):
            for relation in pydiet.nutrient_flag_relations[nutrient_name]:
                # Update an unset flag in any of the four cases (in order of appearance):
                # 1. The nutrient is non-zero and the flag implies non-zero: Make flag True
                # 2. The nutrient is non-zero and the flag implies zero: Make the flag False
                # 3. The nutrient is zero and the flag implies non-zero: Make the flag False
                # 4. The nutrient is zero and the flag implies zero: Make the flag True
                if new_g_per_subject_g > 0:
                    if relation.implies_has_nutrient:
                        self.set_flag(relation.flag_name, True)
                    elif relation.implies_has_no_nutrient:
                        self.set_flag(relation.flag_name, False)
                elif new_g_per_subject_g == 0:
                    if relation.implies_has_nutrient:
                        self.set_flag(relation.flag_name, False)
                    elif relation.implies_has_no_nutrient:
                        self.set_flag(relation.flag_name, True)

    def set_nutrient_pref_unit(self, nutrient_name: str, pref_unit: str) -> None:
        """Sets the pref unit for the nutrient ratio."""
        nutrient_ratio = self.get_nutrient_ratio(nutrient_name)
        nutrient_ratio.pref_unit = pref_unit

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
                if child_rolling_total > parent_nutrient_ratio.g_per_subject_g * 1.01:
                    raise nutrients.exceptions.ChildNutrientQtyExceedsParentNutrientQtyError(
                        'The qty of child nutrients of {} exceed its own mass'.format(parent_nutrient_name))
