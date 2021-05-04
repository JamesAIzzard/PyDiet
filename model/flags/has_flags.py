import abc
from typing import Dict, List, Union, Optional, Any

import model
import persistence

FlagDOFData = Dict[str, Optional[bool]]


class HasFlags(model.nutrients.HasNutrientRatios, persistence.YieldsPersistableData, abc.ABC):
    """Models an object which has flag_data to characterise its content.
    Flags are either direct alias or not. A direct alias flag will derive its value entirely from a
    nutrient ratio on the same instance. For example, "caffiene-free" derives its value entirely from
    the presence of caffiene in the nutrient ratios list. However, flags such as "vegan" are not
    direct aliases, and therefore have a "degree of freedom" or DOF. This allows them to store their
    True/False/None value independently of any nutrient ratios. A flag which is not a direct
    alias cannot have a True value if any related nutrients are conflicting. However, it may have a
    False value even if all of its related nutrients do not conflict. Equally, it may have an undefined
    value even if all of its related nutrients are defined.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # # Check that this isntance also has nutrient ratios;
        # if not isinstance(self, model.nutrients.HasNutrientRatios):
        #     raise TypeError('HasFlags requires NutrientRatios to function.')

    @property
    @abc.abstractmethod
    def _flag_dofs(self) -> 'FlagDOFData':
        """Returns a dictionary of each non-direct alias flag."""
        raise NotImplementedError

    def _get_flag_dof(self, flag_name: str) -> Optional[bool]:
        """Returns the degree of freedom associated with the flag. See notes in class docstring for brief
        description of flag degrees of freedom."""

        flag = model.flags.get_flag(flag_name)

        # Check the flag should have a DOF;
        if flag.direct_alias:
            raise model.flags.exceptions.FlagHasNoDOFError(
                subject=self,
                flag_name=flag_name
            )

        # OK, go ahead and return it;
        try:
            return self._flag_dofs[flag_name]
        except KeyError:
            # Ahh, we don't have a dof listed, just return None.
            return None

    def get_flag_value(self, flag_name: str) -> bool:
        """Get the value of a particular flag by name."""

        # Validate the flag name, and grab a reference to the flag;
        flag_name = model.flags.validation.validate_flag_name(flag_name)
        flag = model.flags.ALL_FLAGS[flag_name]

        # OK. There are two main groups of scenarios here.
        # 1. The flag is a direct alias (and relies on nutrient ratios only).
        # 2. The flag has its own degree of freedom.

        if flag.direct_alias:
            # OK, we have scenario 1.

            # If any nutrient conflicts regardless of if any related nutrients are undefined, the flag
            # is immediately false.
            any_undefined = False
            for nutrient_name in flag.related_nutrient_names:
                try:
                    nr = self.get_nutrient_ratio(nutrient_name)
                except model.nutrients.exceptions.UndefinedNutrientRatioError:
                    any_undefined = True
                    continue
                if flag.nutrient_ratio_matches_relation(nr) is False:
                    return False

            # If any nutrients are undefined, the flag is undefined.
            if any_undefined:
                raise model.flags.exceptions.UndefinedFlagError(
                    flag_name=flag_name,
                    reason="The flag is a direct alias, and at least one of its related nutrients is undefined."
                )

            # OK, no flags undefined, and no conflits either, return True;
            return True

        elif not flag.direct_alias:
            # OK, we have scenario 2. The flag has its own degree of freedom, but if any nutrients conflict
            # we return False straight away. So check for these now;
            for nutrient_name in flag.related_nutrient_names:
                try:
                    nr = self.get_nutrient_ratio(nutrient_name)
                except model.nutrients.exceptions.UndefinedNutrientRatioError:
                    continue
                if flag.nutrient_ratio_matches_relation(nr) is False:
                    return False

            # OK, no conflicts. At this point, we basically return the DOF, unless its undefined?
            if self._get_flag_dof(flag_name) is None:
                raise model.flags.exceptions.UndefinedFlagError(
                    flag_name=flag_name,
                    reason="The flag is not a direct alias, but its degree of freedom is undefined."
                )

            # Cool, it's defined, so just return the DOF;
            return self._get_flag_dof(flag_name)

    def get_undefined_flag_names(self) -> List[str]:
        """Returns a list of all flag names that are undefined."""
        undefined_flags = []
        for flag_name in model.flags.ALL_FLAGS.keys():
            try:
                _ = self.get_flag_value(flag_name)
            except model.flags.exceptions.UndefinedFlagError:
                undefined_flags.append(flag_name)
        return undefined_flags

    @property
    def persistable_data(self) -> Dict[str, Any]:
        # Grab the peristable data from the sibling classes;
        data = super().persistable_data
        data['flag_data'] = self._flag_dofs
        return data


class HasSettableFlags(HasFlags, model.nutrients.HasSettableNutrientRatios, persistence.CanLoadData):
    """Models an object with configurable flag_data to characterise its content."""

    def __init__(self, flag_data: Optional['FlagDOFData'] = None, **kwargs):
        super().__init__(**kwargs)

        self._flag_dof_data: 'FlagDOFData' = {}

        if flag_data is not None:
            self.load_data({'flag_data': flag_data})

    @property
    def _flag_dofs(self) -> 'FlagDOFData':
        return self._flag_dof_data

    def _collect_nutrient_ratio_conflicts(self, flag_name: str,
                                          flag_value: Optional[bool]) -> 'model.flags.NRConflicts':
        """Collects and groups any conflicts which would arise between the proposed flag
        and value, and the current nutrient ratio data on the instance.

        Returns:
            conflicts (NRConflicts): Dict containing four lists of nutrient ratios which
            would conflict, see NRConflicts class docstring for more info.
        Notes:
            If the flag is a direct alias, associated nutrients that are not defined will be
            returned as conflicts. If the flag is not a direct alias, associated nutrients that are
            not defined are not counted as conflicts, because the flag's DOF can override them.
        """

        # Validate the params;
        flag_name = model.flags.validation.validate_flag_name(flag_name)
        flag_value = model.flags.validation.validate_flag_value(flag_value)

        # Init the conflits dict structure;
        conflicts = model.flags.NRConflicts(
            need_zero=[],
            need_non_zero=[],
            need_undefining=[],
            preventing_flag_undefine=[]
        )

        # Grab a reference to the flag thats involved;
        flag = model.flags.ALL_FLAGS[flag_name]

        # OK, lets split into the three main scenarios now. There is a different scenario for each
        # possible proposed value for the flag to be set to. This is going to be complicated, so take a
        # few deep breaths.

        # 1. Flag is being set to True:
        if flag_value is True:
            # OK, lets loop through the related nutrient names, and try to grab their ratios;
            for related_nutrient_name in flag.related_nutrient_names:
                # Grab the implication for this nutrient;
                implication = flag.get_implication_for_nutrient(related_nutrient_name)

                # Go ahead and grab the nutrient ratio;
                try:
                    nutrient_ratio = self.get_nutrient_ratio(nutrient_name=related_nutrient_name)

                # Hmmmm, that nutrient ratio wasn't defined;
                except model.nutrients.exceptions.UndefinedNutrientRatioError:
                    # Well, that's only a problem if the flag is a direct alias;
                    if flag.direct_alias:
                        # OK, it was a direct alias, so we have to count this as a conflict;
                        # Remember - our flag value is True here, so the nutrient name goes in the list
                        # that MATCHES the implication.
                        if implication is model.flags.FlagImpliesNutrient.zero:
                            conflicts["need_zero"].append(related_nutrient_name)
                        elif implication is model.flags.FlagImpliesNutrient.non_zero:
                            conflicts["need_non_zero"].append(related_nutrient_name)
                    continue

                # We got this far, so we must have got the nutrient ratio instance.
                # We only need to worry now if the nutrient ratio doesn't match the implication;
                # Again, the proposed flag value is True here, so any conflicts go in the lists
                # that MATCH their implications.
                # noinspection PyUnboundLocalVariable
                if flag.nutrient_ratio_matches_relation(nutrient_ratio) is False:
                    if implication is model.flags.FlagImpliesNutrient.zero:
                        conflicts["need_zero"].append(related_nutrient_name)
                    elif implication is model.flags.FlagImpliesNutrient.non_zero:
                        conflicts["need_non_zero"].append(related_nutrient_name)

        # 2. Flag is being set to False:
        if flag_value is False:
            # OK, lets loop through the related nutrient names, and try to grab their ratios;
            for related_nutrient_name in flag.related_nutrient_names:
                # Grab the implication for this nutrient;
                implication = flag.get_implication_for_nutrient(related_nutrient_name)

                # Go ahead and grab the nutrient ratio;
                try:
                    nutrient_ratio = self.get_nutrient_ratio(nutrient_name=related_nutrient_name)

                # Hmmmm, that nutrient ratio wasn't defined;
                except model.nutrients.exceptions.UndefinedNutrientRatioError:
                    # Well, that's only a problem if the flag is a direct alias;
                    if flag.direct_alias:
                        # OK, it was a direct alias, so we have to count this as a conflict;
                        # Remember - our flag value is False now, so the nutrient name goes in the list
                        # that is OPPOSITE to the implication.
                        if implication is model.flags.FlagImpliesNutrient.zero:
                            conflicts["need_non_zero"].append(related_nutrient_name)
                        elif implication is model.flags.FlagImpliesNutrient.non_zero:
                            conflicts["need_zero"].append(related_nutrient_name)
                    continue

                # We got this far, so we must have got the nutrient ratio instance.
                # Because we are setting the flag to False, we only have a problem if the flag DOES
                # match the implication. This also means any conflicts go in the lists that OPPOSE
                # their implications.
                # noinspection PyUnboundLocalVariable
                if flag.nutrient_ratio_matches_relation(nutrient_ratio) is True:
                    if implication is model.flags.FlagImpliesNutrient.zero:
                        conflicts["need_non_zero"].append(related_nutrient_name)
                    elif implication is model.flags.FlagImpliesNutrient.non_zero:
                        conflicts["need_zero"].append(related_nutrient_name)

        # 3. Flag is being undefined:
        if flag_value is None:
            # OK, lets loop through the related nutrient names, and try to grab their ratios;
            for related_nutrient_name in flag.related_nutrient_names:
                # Go ahead and grab the nutrient ratio;
                try:
                    nutrient_ratio = self.get_nutrient_ratio(nutrient_name=related_nutrient_name)

                # That nutrient ratio wasn't defined;
                except model.nutrients.exceptions.UndefinedNutrientRatioError:
                    # Thats good! we're undefining the flag too, so we don't need to worry.
                    continue

                # Ahhh, that nutrient ratio is actually defined.
                # OK, what we do now depends on wether or not the flag is a direct alias. If it is a direct
                # alias, we'll definately need to undefine the nutriet ratio if our flag is to be undefined.
                if flag.direct_alias:
                    # OK, so it is a direct alias. We'll need to count this as a conflict. It needs
                    # to be undefined.
                    conflicts['need_undefining'].append(related_nutrient_name)

                # On the other hand, if it isn't a direct alias, we just need to check it doesn't disagree
                # with the flag;
                if flag.nutrient_ratio_matches_relation(nutrient_ratio) is False:
                    # Ahh OK, it does collide. We'll need to unset this nutrient ratio then.
                    conflicts['need_undefining'].append(related_nutrient_name)

                # If we logged our related nutrient as needing undefining, we need to check we don't have a
                # further problem. If we have more than one nutrient ratio that would need undefining, we
                # actually can't correct this situation, because we don't know which one(s) we actually
                # need to undefine. In this situation, In this situation, we also need to add this situation
                # to the preventing undefine list;
                if related_nutrient_name in conflicts['need_undefining'] and len(conflicts['need_undefining']) > 1:
                    conflicts['preventing_flag_undefine'].append(related_nutrient_name)

        # Thats it! That was complicated. All you have to do now is return the conflicts object,
        # then you can go and have a rest.
        return conflicts

    def set_flag_value(self, flag_name: str,
                       flag_value: Optional[bool],
                       can_modify_nutrients: bool = False) -> None:
        """Sets a flag value by name."""

        # Start by validating the inputs;
        flag_name = model.flags.validation.validate_flag_name(flag_name)
        flag_value = model.flags.validation.validate_flag_value(flag_value)

        # Grab the flag instance;
        flag = model.flags.ALL_FLAGS[flag_name]

        # If flag_value matches the current state, do nothing;
        try:
            if flag_value is self.get_flag_value(flag_name):
                return None
        except model.flags.exceptions.UndefinedFlagError:
            # OK, the flag hasn't been set yet, so don't worry about checking its current state;
            pass

        # Classify the nutrient conflict state;
        nr_conflicts = self._collect_nutrient_ratio_conflicts(flag_name, flag_value)

        # Raise exceptions for the non-fixable error states;
        if len(nr_conflicts['need_non_zero']):
            raise model.exceptions.NonZeroNutrientRatioConflictError(
                flag_name=flag_name,
                flag_value=flag_value,
                conflicting_nutrient_ratios=nr_conflicts['need_non_zero']
            )
        if len(nr_conflicts['preventing_flag_undefine']):
            raise model.exceptions.UndefineMultipleNutrientRatiosError(
                flag_name=flag_name,
                flag_value=flag_value,
                conflicting_nutrient_ratios=nr_conflicts['preventing_flag_undefine']
            )

        # Get permission to address fixable error states;
        if (len(nr_conflicts['need_zero']) or len(nr_conflicts['need_undefining'])) and not can_modify_nutrients:
            raise model.exceptions.FixableNutrientRatioConflictError(
                flag_name=flag_name,
                flag_value=flag_value,
                conflicting_nutrient_ratios=nr_conflicts['need_zero'] + nr_conflicts['need_undefining']
            )

        # Correct the error states and make the change;
        s: Union['HasSettableFlags', 'model.nutrients.HasSettableNutrientRatios'] = self
        for nutrient_ratio_name in nr_conflicts['need_undefining']:
            s.undefine_nutrient_ratio(nutrient_ratio_name)
        for nutrient_ratio_name in nr_conflicts['need_zero']:
            s.zero_nutrient_ratio(nutrient_ratio_name)

        # Finally, set the flag's dof if flag is not a direct alias;
        if not flag.direct_alias:
            self._flag_dofs[flag_name] = flag_value

    def load_data(self, data: Dict[str, Any]) -> None:
        # Pass the data on for sibling classes to load it;
        super().load_data(data)

        # If we don't have any fields in this data, exit;
        if 'flag_data' not in data.keys():
            return

        # Now load the flag DOF's into this instance;
        for flag_name, flag_value in data['flag_data'].items():
            # Only import the flag if it has a DOF. This is important for importing legacy data;
            if not model.flags.flag_has_dof(flag_name):
                continue
            # Go ahead and assign the value;
            self._flag_dof_data[flag_name] = flag_value
