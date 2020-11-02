import abc
from typing import Optional

# Actually, I don't think this is a very smart approach.
# HasUniqueName would 'only' ship with persistable objects, so why not incorporate it
# as an integral part of the SupportsPersistence ABC?

class HasUniqueName(abc.ABC):

    def __init__(self, **kwds):
        self._name: Optional[str] = None

    @property
    def name(self) -> Optional[str]:
        return self._name

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


class HasSettableUniqueName(HasUniqueName, abc.ABC):

    @abc.abstractmethod
    def set_name(self, name: Optional[str]) -> None:
        raise NotImplementedError
