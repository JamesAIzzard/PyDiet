import abc
from typing import Dict, List, Optional

from pydiet.flags import configs, validation
from pydiet.nutrients import HasNutrientRatios, HasSettableNutrientRatios


class HasFlags(HasNutrientRatios, abc.ABC):
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


class HasSettableFlags(HasFlags, HasSettableNutrientRatios, abc.ABC):
    """Models an object with configurable flags to characterise its content."""

    def __init__(self, **kwds):
        super().__init__(**kwds)

    def set_flags(self, flag_data: Dict[str, Optional[bool]]):
        """Sets flags values on the object."""
        for flag_name, flag_value in flag_data.items():
            self.set_flag(flag_name, flag_value)

    def set_flag(self, flag_name: str, flag_value: Optional[bool]) -> None:
        """Sets a flag value by name."""
        # Validate;
        flag_name = validation.validate_flag_name(flag_name)
        flag_value = validation.validate_flag_value(flag_value)

        # Deal with any nutrient-flag relations;
        if flag_name in configs.flag_nutrient_relations:
            relation = configs.flag_nutrient_relations[flag_name]
            for nutrient_name, has_nutrient in relation.items():
                if has_nutrient is False and self.nutrient_g_per_subject_g(nutrient_name) > 0:
                    self.set_nutrient_ratio(nutrient_name=nutrient_name,
                                            nutrient_qty=0,
                                            nutrient_qty_unit='g',
                                            subject_qty=1,
                                            subject_qty_unit='g')
                elif has_nutrient is True and self.nutrient_g_per_subject_g(nutrient_name) == 0:
                    self.undefine_nutrient_ratio(nutrient_name)

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
