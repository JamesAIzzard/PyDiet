import abc
from typing import Optional


class SupportsName(abc.ABC):

    @property
    @abc.abstractmethod
    def name(self) -> Optional[str]:
        raise NotImplementedError

    @property
    def name_is_defined(self) -> bool:
        if self.name is None:
            return False
        else:
            return True

    @property
    def name_summary(self) -> str:
        if self.name_is_defined:
            return self.name
        else:
            return 'Undefined'


class SupportsNameSetting(SupportsName, abc.ABC):

    @abc.abstractmethod
    def set_name(self, name: Optional[str]) -> None:
        raise NotImplementedError
