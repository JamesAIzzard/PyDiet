import abc
from abc import abstractmethod
from typing import Optional, cast

from pydiet import defining

class SupportsName(abc.ABC):

    @property
    @abc.abstractmethod
    def _name(self) -> Optional[str]:
        raise NotImplementedError

    @property
    def name(self) -> str:
        if not self.name_is_defined:
            raise defining.exceptions.NameUndefinedError
        return cast(str, self._name)

    @property
    def name_is_defined(self) -> bool:
        if self._name == None:
            return False
        else:
            return True

    @property
    def name_summary(self) -> str:
        if self.name_is_defined:
            return self.name
        else:
            return 'Undefined'

class SupportsNameSetting(SupportsName):

    @abstractmethod
    def set_name(self, name:str) -> None:
        raise NotImplementedError