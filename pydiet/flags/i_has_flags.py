import abc
from typing import List

from pydiet import flags

class IHasFlags(abc.ABC):

    @abc.abstractproperty
    def flags(self)->List[str]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_flag(self, flag_name:str)->None:
        raise NotImplementedError

    @abc.abstractmethod
    def remove_flag(self, flag_name:str)->None:
        raise NotImplementedError

    @property
    def available_flags(self) ->List[str]:
        # Make a copy of the all flags list so we don't
        # modify the original;
        all_flags = flags.configs.FLAGS.copy()
        for flag_name in self.flags:
            all_flags.remove(flag_name)
        return all_flags



