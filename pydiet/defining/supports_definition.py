import abc
from typing import List, Protocol

class SupportsDefinition(Protocol):

    @property
    def defined(self) -> bool:
        if len(self.missing_mandatory_attrs):
            return False
        else:
            return True

    @abc.abstractproperty
    def missing_mandatory_attrs(self) -> List[str]:
        raise NotImplementedError