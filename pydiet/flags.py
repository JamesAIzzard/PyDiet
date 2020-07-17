import abc
from typing import List

import pydiet
from pydiet.ingredients import ingredient_service

FLAGS = [
    "alcohol_free",
    "caffiene_free",
    "dairy_free",
    "gluten_free",
    "nut_free",
    "vegan",
    "vegetarian"
]

class IFlaggable(abc.ABC):

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

def print_active_flags_menu(subject:'IFlaggable'):
    output = ''
    if len(subject.flags):
        for i,flag_name in enumerate(subject.flags, start=1):
            output = output + '{num}. {flag_name}\n'.format(
                num=i,
                flag_name=flag_name)
    else:
        output = 'No flags assigned.'
    return output

class FlagNameError(pydiet.PyDietException):
    pass