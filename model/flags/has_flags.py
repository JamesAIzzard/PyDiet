import abc
from typing import Dict, List, Optional

from model import nutrients, flags


class HasFlags(abc.ABC):
    """Models an object which has flag_data to characterise its content."""

    def __init__(self, flag_data: Dict[str, Optional[bool]], **kwargs):
        super().__init__(**kwargs)
        # Build the internal flag list;
        # First build the keys up;
        self._flags = {flag_name: None for flag_name in flags.configs.all_flags.keys()}
        # Now import the values;
        for flag_name, flag_value in flag_data.items():
            # Catch error where flag name is not recognised;
            if flag_name not in self._flags.keys():
                raise ValueError(f"{flag_name} is not a recognised flag name.")
            # Go ahead and assign the value;
            self._flags[flag_name] = flag_value

    @property
    def all_flag_names(self) -> List[str]:
        """Returns a list of all flag names."""
        return list(self._flags.keys())

    def get_flag_value(self, flag_name: str) -> Optional[bool]:
        """Get the value of a particular flag by name."""
        return self._flags[flag_name]

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

    def set_flags(self, flag_data: Dict[str, Optional[bool]]):
        """Sets flag_data values on the object."""
        for flag_name, flag_value in flag_data.items():
            self.set_flag(flag_name, flag_value)

    def set_flag(self, flag_name: str, flag_value: Optional[bool]) -> None:
        """Sets a flag value by name."""
        # Validate;
        # flag_name = flags.validation.validate_flag_name(flag_name)
        # flag_value = flags.validation.validate_flag_value(flag_value)

        raise NotImplementedError

    def set_all_flags_true(self) -> None:
        """Sets all flag_data to be True."""
        for flag_name in self._flags:
            self.set_flag(flag_name, True)

    def set_all_flags_false(self) -> None:
        """Sets all flag_data to be False."""
        for flag_name in self._flags:
            self.set_flag(flag_name, False)
