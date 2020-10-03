import abc
import copy
from typing import Dict, List, Optional, Any

from pydiet import flags, nutrients


def get_empty_flags_data() -> Dict[str, Optional[bool]]:
    empty_flags_data = {}
    for flag_name in flags.configs.all_flag_names:
        empty_flags_data[flag_name] = None
    return empty_flags_data


class SupportsFlags(nutrients.supports_nutrient_content.SupportsSettingNutrientContent, abc.ABC):

    @property
    @abc.abstractmethod
    def _flags_data(self) -> Dict[str, Optional[bool]]:
        raise NotImplementedError

    @property
    def flags_data_copy(self) -> Dict[str, Optional[bool]]:
        return copy.deepcopy(self._flags_data)

    @property
    def flags_summary(self) -> str:
        output = ''
        for fname in self._flags_data:
            output = output + '{name:<15} {value:<10}\n'.format(
                name=fname.replace('_', ' ') + ':',
                value=self.summarise_flag(fname)
            )
        return output

    @property
    def all_flag_names(self) -> List[str]:
        return list(self._flags_data.keys())

    def get_flag_value(self, flag_name: str) -> Optional[bool]:
        return self.flags_data_copy[flag_name]

    def _filter_flags(self, filter_value: Optional[bool]) -> List[str]:
        return_flag_names = []
        for flag_name in self.flags_data_copy.keys():
            if self.flags_data_copy[flag_name] == filter_value:
                return_flag_names.append(flag_name)
        return return_flag_names

    @property
    def true_flags(self) -> List[str]:
        return self._filter_flags(True)

    @property
    def false_flags(self) -> List[str]:
        return self._filter_flags(False)

    @property
    def unset_flags(self) -> List[str]:
        return self._filter_flags(None)

    @property
    def all_flags_undefined(self) -> bool:
        return True in self._flags_data.values() or False in self._flags_data.values()

    @property
    def any_flag_undefined(self) -> bool:
        return None in self._flags_data.values()

    @staticmethod
    def validate_flag_value(value: Any) -> Optional[bool]:
        if value not in [True, False, None]:
            raise flags.exceptions.FlagValueError
        return value

    @staticmethod
    def validate_flag_name(name: str) -> str:
        if name.lower() not in flags.configs.all_flag_names:
            raise flags.exceptions.FlagNameError
        return name.lower()

    def flag_is_defined(self, flag_name: str) -> bool:
        return self._flags_data[flag_name] is not None

    def summarise_flag(self, flag_name: str) -> str:
        val = self.get_flag_value(flag_name)
        if val is None:
            return 'Undefined'
        else:
            return str(val)


class SupportsFlagSetting(SupportsFlags, abc.ABC):

    def set_flags(self, flag_data: Dict[str, Optional[bool]]):
        for fname in flag_data:
            self.set_flag(fname, flag_data[fname])

    def set_flag(self, flag_name: str, flag_value: Optional[bool]) -> None:
        # Validate;
        flag_name = self.validate_flag_name(flag_name)
        flag_value = self.validate_flag_value(flag_value)

        # If the flag is true, zero any nutrients related to it;
        zero_data = nutrients.supports_nutrient_content.NutrientData(
            nutrient_g_per_subject_g=0,
            nutrient_pref_units='g'
        )
        if flag_name in nutrients.configs.nutrient_flag_rels:
            for related_nutrient in nutrients.configs.nutrient_flag_rels[flag_name]:
                if flag_value is True:
                    self.set_nutrient_data(related_nutrient, zero_data)
                else:
                    if self.get_nutrient_data_copy(related_nutrient)['nutrient_g_per_subject_g'] == 0:
                        self.reset_nutrient(related_nutrient)

        # Set;
        self._flags_data[flag_name] = flag_value

    def set_all_flags_yes(self) -> None:
        for flag_name in self._flags_data:
            self.set_flag(flag_name, True)

    def set_all_flags_no(self) -> None:
        for flag_name in self._flags_data:
            self.set_flag(flag_name, False)
