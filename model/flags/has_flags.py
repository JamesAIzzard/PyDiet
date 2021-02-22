import abc
from typing import Dict, List, Union, TypedDict, Optional

from model import nutrients, flags


class NRConflicts(TypedDict):
    need_zero: List['nutrients.NutrientRatio']
    need_none: List['nutrients.NutrientRatio']
    need_non_zero: List['nutrients.NutrientRatio']
    preventing_undefine: List['nutrients.NutrientRatio']


class HasFlags(abc.ABC):
    """Models an object which has flag_data to characterise its content."""

    def __init__(self, flag_data: Optional[Dict[str, Optional[bool]]] = None, **kwargs):
        super().__init__(**kwargs)

        # Build a dict for all flags which are not direct_alias
        self._flag_dofs: Dict[str, Optional[bool]] = {}
        for flag_name, flag in flags.all_flags.items():
            if flag.direct_alias:
                self._flag_dofs[flag_name] = None

        # Note, this implementation is good, becuase it means if we add a flag to the global list
        # after this instance has been saved, the new flag will automatically be added when this
        # instance is re-saved.

        # Now import the values, if present;
        if flag_data is not None:
            for flag_name, flag_value in flag_data.items():
                # Catch error where flag name is not recognised;
                if flag_name not in self._flag_dofs.keys():
                    raise ValueError(f"{flag_name} is not a recognised flag name.")
                # Catch dofs for flags which are direct aliases;
                if flags.all_flags[flag_name].direct_alias:
                    raise flags.exceptions.UnexpectedFlagDOFError(flag_name=flag_name)
                # Go ahead and assign the value;
                self._flag_dofs[flag_name] = flag_value

    @property
    def flags_dof_data(self) -> Dict[str, Optional[bool]]:
        """Returns a dictionary of the flag names and their dof states"""
        return {flag_name: flag_dof_value for flag_name, flag_dof_value in self._flag_dofs.items()}

    def gather_related_nutrient_ratios(self, flag_name: str) -> List['nutrients.NutrientRatio']:
        """Returns a list of nutrient ratios, from this instance, that are related to the named flag."""

        # Check that we have nutrient ratios on this instance;
        # Confirm we have settable nutrient ratios too;
        if not isinstance(self, nutrients.HasSettableNutrientRatios):
            raise AttributeError('Readable nutrient ratios are required to use flags.')

        # Validate the flag name;
        flag_name = flags.validation.validate_flag_name(flag_name)
        # Grab a reference to the global flag;
        flag = flags.all_flags[flag_name]
        # Now build up a list of this instance's related nutrient ratios;
        related_nutrient_names = flag.related_nutrient_names
        # Grab related nutrient ratios;
        related_nutrient_ratios: List['nutrients.NutrientRatio'] = []
        for related_nutrient_name in related_nutrient_names:
            related_nutrient_ratios.append(self.get_nutrient_ratio(related_nutrient_name))

        return related_nutrient_ratios

    def get_flag_value(self, flag_name: str) -> Optional[bool]:
        """Get the value of a particular flag by name."""

        # First, check that I also have readable nutrient ratios;
        if not isinstance(self, (nutrients.HasNutrientRatios, HasFlags)):
            raise AttributeError('Readable nutrient ratios are requried to use flags.')

        # Validate the flag name, and grab a reference to the flag;
        flag_name = flags.validation.validate_flag_name(flag_name)
        flag = flags.all_flags[flag_name]

        # Grab related nutrient ratios;
        related_nutrient_ratios = self.gather_related_nutrient_ratios(flag_name)

        # Loop through the nutrients and check for mismatch or undefined nutrients;
        for related_nutrient_ratio in related_nutrient_ratios:
            if flag.nutrient_ratio_matches_relation(related_nutrient_ratio) is True:
                continue
            elif flag.nutrient_ratio_matches_relation(related_nutrient_ratio) is False:
                return False
            elif flag.nutrient_ratio_matches_relation(related_nutrient_ratio) is None:
                if flag.direct_alias:
                    return None
                else:
                    continue

        # Finished looping through all related nutrients, so flag must match nutrient states;
        return True

    def _filter_flags(self, filter_value: Optional[bool]) -> List[str]:
        """Gets flag_data names by value."""
        return_flag_names = []
        for flag_name in flags.all_flags.keys():
            if self.get_flag_value(flag_name) == filter_value:
                return_flag_names.append(flag_name)
        return return_flag_names

    @property
    def true_flags(self) -> List[str]:
        """Returns a list of all flag_data with value set to True."""
        return self._filter_flags(True)

    @property
    def false_flags(self) -> List[str]:
        """Returns a list of all flag_data with value set to False."""
        return self._filter_flags(False)

    @property
    def unset_flags(self) -> List[str]:
        """Returns a list of all flag_data which are undefined."""
        return self._filter_flags(None)

    # todo - Got to here while correcting the old usage of flag_dofs.

    @property
    def all_flags_undefined(self) -> bool:
        """Returns True/False to indicate if all flag_data are undefined."""
        return True not in self._flag_dofs.values() and False not in self._flag_dofs.values()

    @property
    def any_flag_undefined(self) -> bool:
        """Returns True/False to indicate if any flag is undefined."""
        return None in self._flag_dofs.values()

    def flag_is_defined(self, flag_name: str) -> bool:
        """Returns True/False to indicate if a flag is undefined by name."""
        return self._flag_dofs[flag_name] is not None

    def flag_is_true(self, flag_name: str) -> bool:
        """Returns True/False to indicate if the named flag is True."""
        return self._flag_dofs[flag_name] is True

    def flag_is_false(self, flag_name: str) -> bool:
        """Returns True/False to indicate if the named flag is False."""
        return self._flag_dofs[flag_name] is False


class HasSettableFlags(HasFlags, abc.ABC):
    """Models an object with configurable flag_data to characterise its content."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def analyse_nutrient_ratio_conflicts(self, flag_name: str, flag_value: Optional[bool]) -> 'NRConflicts':
        """Collects and groups any conflicts which would arise between the proposed flag
        and value, and the current nutrient ratio data on the instance.

        Returns:
            conflicts (NRConfclicts): Dict containing three lists of nutrient ratios which
            would conflict, grouped into three different lists. The lists are:
                - need_zero -> These nutrients ratios would need to be zero for the flag to apply.
                - need_none -> The single nutrient ratio associated with a flag being set to None.
                - need_non_zero -> These nutrient ratios would need to be non zero for the flag to apply.
                - preventing_undefine -> The multiple nutrient ratios that mean we can't set the flag to be undefined.
        Notes:
            If the related flag is a direct alias, associated nutrients that are not defined will be
            returned as conflicts. If the flag is not a direct alias, associated nutrients that are
            not defined are not counted as conflicts, because the flag's DOF can override them.
        """

        # Check we also have nutrient ratios;
        # Confirm we have settable nutrient ratios too;
        if not isinstance(self, nutrients.HasSettableNutrientRatios):
            raise AttributeError('Readable nutrient ratios are required to analyse flag conflicts.')
        self: Union['HasSettableFlags', 'nutrients.HasNutrientRatios']  # Force mixin code analysis.

        # Validate the params;
        flag_name = flags.validation.validate_flag_name(flag_name)
        flag_value = flags.validation.validate_flag_value(flag_value)

        # Init the conflits dict structure;
        conflicts = NRConflicts(
            need_none=[],
            need_zero=[],
            need_non_zero=[],
            preventing_undefine=[]
        )

        # Analyse nutrients related to this flag, grouping any conflicts;
        flag = flags.all_flags[flag_name]
        related_nutrient_names = flag.related_nutrient_names
        for related_nutrient_name in related_nutrient_names:
            nutrient_ratio = self.get_nutrient_ratio(nutrient_name=related_nutrient_name)
            implication = flag.get_implication_for_nutrient(related_nutrient_name)
            if flag_value is None:
                if nutrient_ratio.defined:
                    if flag.direct_alias:
                        # If we have only found one nutrient which needs undefining, add it to the
                        # need_none list.
                        if len(conflicts['need_none']) == 0 and len(conflicts['preventing_undefine']) == 0:
                            conflicts['need_none'].append(nutrient_ratio)
                        # If there is already a nutrient in the undefine list, move it to preventing_undefine
                        # and add this next one to preventing_undefine;
                        elif len(conflicts['need_none']) == 1 and len(conflicts['preventing_undefine']) == 0:
                            conflicts['preventing_undefine'].append(conflicts['need_none'].pop())
                            conflicts['preventing_undefine'].append(nutrient_ratio)
                        # If we already have one on preventing_undefine, then just keep adding to it.
                        elif len(conflicts['need_none']) == 0 and len(conflicts['preventing_undefine']) > 0:
                            conflicts['preventing_undefine'].append(nutrient_ratio)
            elif flag_value is True:
                if implication is implication.zero:
                    if nutrient_ratio.is_non_zero:
                        conflicts['need_zero'].append(nutrient_ratio)
                    elif nutrient_ratio.undefined and flag.direct_alias:
                        conflicts['need_zero'].append(nutrient_ratio)
                elif implication is implication.non_zero:
                    if nutrient_ratio.is_zero:
                        conflicts['need_non_zero'].append(nutrient_ratio)
                    elif nutrient_ratio.undefined and flag.direct_alias:
                        conflicts['need_non_zero'].append(nutrient_ratio)
            elif flag_value is False:
                if implication is implication.zero:
                    if nutrient_ratio.is_zero:
                        conflicts['need_non_zero'].append(nutrient_ratio)
                    elif nutrient_ratio.undefined and flag.direct_alias:
                        conflicts['need_non_zero'].append(nutrient_ratio)
                elif implication is implication.non_zero:
                    if nutrient_ratio.is_non_zero:
                        conflicts['need_zero'].append(nutrient_ratio)
                    elif nutrient_ratio.undefined and flag.direct_alias:
                        conflicts['need_zero'].append(nutrient_ratio)

        return conflicts

    def set_flag_values(self, flag_data: Dict[str, Optional[bool]]):
        """Sets flag_data values on the object."""
        for flag_name, flag_value in flag_data.items():
            self.set_flag_value(flag_name, flag_value)

    def set_flag_value(self, flag_name: str,
                       flag_value: Optional[bool],
                       can_modify_nutrients: bool = False) -> None:
        """Sets a flag value by name."""

        # Confirm we have settable nutrient ratios too;
        if not isinstance(self, nutrients.HasSettableNutrientRatios):
            raise AttributeError('Writeable nutrient ratios are required to set flags.')
        self: Union['HasSettableFlags', 'nutrients.HasSettableNutrientRatios']  # Force mixin code analysis.

        # Start by validating the inputs;
        flag_name = flags.validation.validate_flag_name(flag_name)
        flag_value = flags.validation.validate_flag_value(flag_value)

        # Grab the flag instance;
        flag = flags.all_flags[flag_name]

        # If flag_value matches the current state, do nothing;
        if flag_value is self.get_flag_value(flag_name):
            return None

        # Classify nutrient conflict state;
        nr_conflicts = self.analyse_nutrient_ratio_conflicts(flag_name, flag_value)

        # Catch the non-fixable error states;
        if len(nr_conflicts['need_non_zero']):
            raise flags.exceptions.NonZeroNutrientRatioConflictError(
                flag_name=flag_name,
                flag_value=flag_value,
                conflicting_nutrient_ratios=nr_conflicts['need_non_zero']
            )
        if len(nr_conflicts['preventing_undefine']):
            raise flags.exceptions.UndefineMultipleNutrientRatiosError(
                flag_name=flag_name,
                flag_value=flag_value,
                conflicting_nutrient_ratios=nr_conflicts['preventing_undefine']
            )

        # Get permission to address fixable error states;
        if (len(nr_conflicts['need_zero']) or len(nr_conflicts['need_none'])) and not can_modify_nutrients:
            raise flags.exceptions.FixableNutrientRatioConflictError(
                flag_name=flag_name,
                flag_value=flag_value,
                conflicting_nutrient_ratios=nr_conflicts['need_zero'] + nr_conflicts['need_none']
            )

        # Correct the error states and make the change;
        for nr in nr_conflicts['need_none']:
            if not isinstance(nr, nutrients.SettableNutrientRatio):
                raise AttributeError("set_flag_value requires settable nutrient ratios.")
            nr.undefine()
        for nr in nr_conflicts['need_zero']:
            if not isinstance(nr, nutrients.SettableNutrientRatio):
                raise AttributeError("set_flag_value requires settable nutrient ratios.")
            nr.zero()

        # Finally, set the flag's dof if flag is not a direct alias;
        if not flag.direct_alias:
            self._flag_dofs[flag_name] = flag_value

    def set_all_flags_true(self) -> None:
        """Sets all flag_data to be True."""
        for flag_name in self._flag_dofs:
            self.set_flag_value(flag_name, True)

    def set_all_flags_false(self) -> None:
        """Sets all flag_data to be False."""
        for flag_name in self._flag_dofs:
            self.set_flag_value(flag_name, False)
