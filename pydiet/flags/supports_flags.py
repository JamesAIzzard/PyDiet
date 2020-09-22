import abc
import copy
from typing import Dict, List, Optional

from pydiet import flags


def get_empty_flags_data() -> Dict[str, Optional[bool]]:
    empty_flags_data = {}
    for flag_name in flags.configs.all_flag_names:
        empty_flags_data[flag_name] = None
    return empty_flags_data


class SupportsFlags(abc.ABC):

    @property
    @abc.abstractmethod
    def _flags_data(self) -> Dict[str, Optional[bool]]:
        raise NotImplementedError

    @property
    def flags_data_copy(self) -> Dict[str, Optional[bool]]:
        return copy.deepcopy(self._flags_data)

    @property
    def flags_summary(self) -> str:
        return 'A flag summary.'

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

    def flag_is_defined(self, flag_name: str) -> bool:
        return self._flags_data[flag_name] is not None

    def summarise_flag(self, flag_name:str) -> str:
        val = self.get_flag_value(flag_name)
        if val is None:
            return 'Undefined'
        else:
            return str(val)


class SupportsFlagSetting(SupportsFlags, abc.ABC):

    def set_flag(self, flag_name: str, flag_value: Optional[bool]) -> None:
        if flag_value is None:
            self._flags_data[flag_name] = None
        else:
            self._flags_data[flag_name] = bool(flag_value)
