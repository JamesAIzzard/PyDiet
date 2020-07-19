import abc
from typing import List

class IHasTags(abc.ABC):

    @abc.abstractproperty
    def tags(self) -> List[str]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_tag(self, tag:str)->None:
        raise NotImplementedError

    @abc.abstractmethod
    def remove_tag(self, tag:str)->None:
        raise NotImplementedError