import abc
from typing import List, Dict, Optional

from pydiet import flags

class IHasFlags(abc.ABC):

    @abc.abstractproperty
    def flags(self)->Dict[str, bool]:
        raise NotImplementedError

    @abc.abstractmethod
    def set_flag(self, flag_name:str, flag_status:bool)->None:
        raise NotImplementedError

    def get_flag(self, flag_name: str) -> Optional[bool]:
        return self.flags[flag_name]

    @property
    def true_flags(self) ->List[str]:
        true_flags = []
        for flag_name in self.flags:
            if self.flags[flag_name] == True:
                true_flags.append(flag_name)
        return true_flags

    @property
    def false_flags(self) -> List[str]:
        false_flags = []
        for flag_name in self.flags:
            if self.flags[flag_name] == False:
                false_flags.append(flag_name)
        return false_flags

    @property
    def undefined_flags(self) -> List[str]:
        none_flags = []
        for flag_name in self.flags:
            if self.flags[flag_name] == None:
                none_flags.append(flag_name)
        return none_flags

    @property
    def all_flags_undefined(self) -> bool:
        for flag_name in self.flags:
            if not self.flag_is_defined(flag_name):
                return False
        return True

    def flag_is_defined(self, flag_name) -> bool:
        if self.flags[flag_name] == None:
            return False
        else:
            return True        


