import abc
from typing import Dict, List, Optional, Protocol

from pydiet import flags as flag_module

class SupportsFlags(Protocol):

    @abc.abstractproperty
    def readonly_flag_data(self) -> Dict[str, Optional[bool]]:
        raise NotImplementedError

    def get_flag_value(self, flag_name: str) -> Optional[bool]:
        return self.readonly_flag_data[flag_name]

    def _filter_flags(self, filter_value:Optional[bool]) -> List[str]:
        return_flag_names = []
        for flag_name in self.readonly_flag_data.keys():
            if self.readonly_flag_data[flag_name] == filter_value:
                return_flag_names.append(flag_name)
        return return_flag_names       

    @property
    def true_flags(self) -> List[str]:
        return self._filter_flags(True)

    @property
    def false_flags(self) -> List[str]:
        return self._filter_flags(False)

    @property
    def undefined_flags(self) -> List[str]:
        return self._filter_flags(None)

    @property
    def all_flags_undefined(self) -> bool:
        if len(self.undefined_flags) == len(self.readonly_flag_data):
            return True
        else:
            return False

    def flag_is_defined(self, flag_name:str) -> bool:
        if self.get_flag_value(flag_name).value == None:
            return False
        else:
            return True

class SupportsFlagSetting(SupportsFlags, Protocol):

    @abc.abstractproperty
    def flag_data(self) -> Dict[str, Optional[bool]]:
        raise NotImplementedError

    def set_flag(self, flag_name: str, flag_value: Optional[bool]) -> None:
        if flag_value == None:
            self.flag_data[flag_name] = None
        else:
            self.flag_data[flag_name] = bool(flag_value)
