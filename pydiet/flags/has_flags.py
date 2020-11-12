import abc
from typing import Dict, List, Optional

import pydiet
from pydiet import nutrients
from pydiet.flags import configs, validation


class HasFlags(abc.ABC):
    """Models an object which has flags to characterise its content."""

    def __init__(self, flags: Dict[str, Optional[bool]], **kwds):
        super().__init__(**kwds)
        # Init the internal flags list;
        self._flags = {}
        for flag_name in configs.all_flag_names:
            self._flags[flag_name] = None
        # Load in any legitimate values which were passed in;
        for flag_name, flag_value in flags.items():
            if flag_name in self._flags:  # Prevent unknown flags being set.
                self._flags[flag_name] = flag_value

    @property
    def flags_summary(self) -> str:
        """Returns a readable summary of the flags."""
        output = ''
        for fname in self._flags:
            output = output + '{name:<15} {value:<10}\n'.format(
                name=fname.replace('_', ' ') + ':',
                value=self.summarise_flag(fname)
            )
        return output

    @property
    def all_flag_names(self) -> List[str]:
        """Returns a list of all flag names."""
        return list(self._flags.keys())

    def get_flag_value(self, flag_name: str) -> Optional[bool]:
        """Get the value of a particular flag by name."""
        return self._flags[flag_name]

    def _filter_flags(self, filter_value: Optional[bool]) -> List[str]:
        """Gets flags names by value."""
        return_flag_names = []
        for flag_name in self._flags.keys():
            if self._flags[flag_name] == filter_value:
                return_flag_names.append(flag_name)
        return return_flag_names

    @property
    def true_flags(self) -> List[str]:
        """Returns a list of all flags with value set to True."""
        return self._filter_flags(True)

    @property
    def false_flags(self) -> List[str]:
        """Returns a list of all flags with value set to False."""
        return self._filter_flags(False)

    @property
    def unset_flags(self) -> List[str]:
        """Returns a list of all flags which are undefined."""
        return self._filter_flags(None)

    @property
    def all_flags_undefined(self) -> bool:
        """Returns True/False to indicate if all flags are undefined."""
        return True not in self._flags.values() and False not in self._flags.values()

    @property
    def any_flag_undefined(self) -> bool:
        """Returns True/False to indicate if any flag is undefined."""
        return None in self._flags.values()

    def flag_is_defined(self, flag_name: str) -> bool:
        """Returns True/False to indicate if a flag is undefined by name."""
        return self._flags[flag_name] is not None

    def summarise_flag(self, flag_name: str) -> str:
        """Return a readable summary of the flag by name."""
        val = self.get_flag_value(flag_name)
        if val is None:
            return 'Undefined'
        else:
            return str(val)


class HasSettableFlags(HasFlags, abc.ABC):
    """Models an object with configurable flags to characterise its content."""

    def __init__(self, **kwds):
        super().__init__(**kwds)

        # Check that we don't have readonly nutrient ratios. Having this at the same time as
        # having settable flags would allow inconsistencies.
        if not isinstance(self, nutrients.HasSettableNutrientRatios):
            assert not isinstance(self, nutrients.HasNutrientRatios)

    def set_flags(self, flag_data: Dict[str, Optional[bool]]):
        """Sets flags values on the object."""
        for flag_name, flag_value in flag_data.items():
            self.set_flag(flag_name, flag_value)

    def set_flag(self, flag_name: str, flag_value: Optional[bool]) -> None:
        """Sets a flag value by name."""
        # Validate;
        flag_name = validation.validate_flag_name(flag_name)
        flag_value = validation.validate_flag_value(flag_value)

        # Shout if there is a defined and conflicting nutrient ratio (hard conflicts);
        if isinstance(self, nutrients.HasNutrientRatios):
            for relation in pydiet.get_nutrient_relations[flag_name]:
                nutrient_ratio = self.get_nutrient_ratio(nutrient_name=relation.nutrient_name)
                if relation.asserts_has_nutrient and nutrient_ratio.is_zero:
                    raise pydiet.exceptions.FlagNutrientConflictError(
                        '{flag_name} implies {nutrient_name}% should be zero.'.format(
                            flag_name=flag_name,
                            nutrient_name=relation.nutrient_name
                        )
                    )
                elif relation.asserts_has_no_nutrient and nutrient_ratio.is_non_zero:
                    raise pydiet.exceptions.FlagNutrientConflictError(
                        '{flag_name} implies {nutrient_name}% should be greater than zero.'.format(
                            flag_name=flag_name,
                            nutrient_name=relation.nutrient_name
                        )
                    )

        # Update any unset and related nutrient ratios (soft conflicts);
        if isinstance(self, nutrients.HasSettableNutrientRatios):
            for relation in pydiet.get_nutrient_relations[flag_name]:
                nutrient_ratio = self.get_nutrient_ratio(nutrient_name=relation.nutrient_name)
                if relation.asserts_has_no_nutrient and nutrient_ratio.not_defined:
                    nutrient_ratio.g_per_subject_g = 0

        # Set;
        self._flags[flag_name] = flag_value

    def set_all_flags_yes(self) -> None:
        """Sets all flags to be True."""
        for flag_name in self._flags:
            self.set_flag(flag_name, True)

    def set_all_flags_no(self) -> None:
        """Sets all flags to be False."""
        for flag_name in self._flags:
            self.set_flag(flag_name, False)
