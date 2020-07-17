import abc
from typing import List

class ITaggable(abc.ABC):

    @abc.abstractproperty
    def tags(self) -> List[str]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_tag(self, tag:str)->None:
        raise NotImplementedError

    @abc.abstractmethod
    def remove_tag(self, tag:str)->None:
        raise NotImplementedError

def print_enumerated_active_tags(subject:'ITaggable')->str:
    output = ''
    if len(subject.tags):
        for i,tag in enumerate(subject.tags, start=1):
            output = output + '{num}. {tag}'.format(
                num=i,
                tag=tag
            )
    else:
        output = 'No tags assigned.'
    return output