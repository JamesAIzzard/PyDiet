import abc
from typing import List

from pydiet.ingredients import ingredient_service

class Flaggable(abc.ABC):

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
        all_flags = ingredient_service.get_all_flag_names()
        for flag_name in self.flags:
            all_flags.remove(flag_name)
        return all_flags