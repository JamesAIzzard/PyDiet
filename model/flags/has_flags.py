import abc
from typing import Dict, List, Optional

from model import nutrients, flags


class HasFlags(abc.ABC):
    """Models an object which has flag_data to characterise its content."""

    def __init__(self, flag_data: Optional[Dict[str, Optional[bool]]] = None, **kwargs):
        super().__init__(**kwargs)

        # Build the internal flag list;
        # First build the keys up;
        self._flags = {flag_name: None for flag_name in flags.all_flags.keys()}

        # Note, this implementation is good, becuase it means if we add a flag to the global list
        # after this instance has been saved, the new flag will automatically be added when this
        # instance is re-saved.

        # Now import the values, if present;
        if flag_data is not None:
            for flag_name, flag_value in flag_data.items():
                # Catch error where flag name is not recognised;
                if flag_name not in self._flags.keys():
                    raise ValueError(f"{flag_name} is not a recognised flag name.")
                # Go ahead and assign the value;
                self._flags[flag_name] = flag_value

    @property
    def flags_data(self) -> Dict[str, Optional[bool]]:
        """Returns a dictionary of the flag names and their states"""
        return {flag_name: flag_value for flag_name, flag_value in self._flags.items()}

    def get_flag_value(self, flag_name: str) -> Optional[bool]:
        """Get the value of a particular flag by name."""

        # First, check that I also have readable nutrient ratios;
        if not isinstance(self, nutrients.HasNutrientRatios):
            raise AttributeError('Readable nutrient ratios are requried to use flags.')

        # Validate the flag name, and grab a reference to the flag;
        flag_name = flags.validation.validate_flag_name(flag_name)
        flag = flags.all_flags[flag_name]

        # Now build up a list of the related nutrient ratios;
        related_nutrient_names = flag.related_nutrient_names
        # Grab related nutrient ratios;
        related_nutrient_ratios: List['nutrients.NutrientRatio'] = []
        for related_nutrient_name in related_nutrient_names:
            related_nutrient_ratios.append(self.get_nutrient_ratio(related_nutrient_name))

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
        for flag_name in self._flags.keys():
            if self._flags[flag_name] == filter_value:
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

    @property
    def all_flags_undefined(self) -> bool:
        """Returns True/False to indicate if all flag_data are undefined."""
        return True not in self._flags.values() and False not in self._flags.values()

    @property
    def any_flag_undefined(self) -> bool:
        """Returns True/False to indicate if any flag is undefined."""
        return None in self._flags.values()

    def flag_is_defined(self, flag_name: str) -> bool:
        """Returns True/False to indicate if a flag is undefined by name."""
        return self._flags[flag_name] is not None

    def flag_is_true(self, flag_name: str) -> bool:
        """Returns True/False to indicate if the named flag is True."""
        return self._flags[flag_name] is True

    def flag_is_false(self, flag_name: str) -> bool:
        """Returns True/False to indicate if the named flag is False."""
        return self._flags[flag_name] is False


class HasSettableFlags(HasFlags, abc.ABC):
    """Models an object with configurable flag_data to characterise its content."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Check that we don't have readonly nutrient ratios. Having this at the same time as
        # having settable flag_data would allow inconsistencies.
        if not isinstance(self, nutrients.HasSettableNutrientRatios):
            assert not isinstance(self, nutrients.HasNutrientRatios)

    def set_flag_values(self, flag_data: Dict[str, Optional[bool]]):
        """Sets flag_data values on the object."""
        for flag_name, flag_value in flag_data.items():
            self.set_flag_value(flag_name, flag_value)

    def set_flag_value(self, flag_name: str, flag_value: Optional[bool]) -> None:
        """Sets a flag value by name."""
        # Start by validating the inputs;
        flag_name = flags.validation.validate_flag_name(flag_name)
        flag_value = flags.validation.validate_flag_value(flag_value)

        # Grab the flag instance;
        flag = flags.all_flags[flag_name]

        # If the flag is direct and matches already, you don't need to do anything;
        if flag.direct_alias and flag.nutrients_match_implied_states:
            return

        raise NotImplementedError

    def set_all_flags_true(self) -> None:
        """Sets all flag_data to be True."""
        for flag_name in self._flags:
            self.set_flag_value(flag_name, True)

    def set_all_flags_false(self) -> None:
        """Sets all flag_data to be False."""
        for flag_name in self._flags:
            self.set_flag_value(flag_name, False)
