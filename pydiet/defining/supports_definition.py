import abc
from typing import List, Optional

class SupportsDefinition(abc.ABC):

    @abc.abstractproperty
    def missing_mandatory_attrs(self) -> List[str]:
        raise NotImplementedError

    @property
    def defined(self) -> bool:
        if len(self.missing_mandatory_attrs):
            return False
        else:
            return True

    @property
    def status_summary(self) -> str:
        if self.defined:
            return 'Complete'
        else:
            return 'Incomplete, needs {}'.format(self.next_attr_to_define)

    @property
    def next_attr_to_define(self) -> Optional[str]:
        if len(self.missing_mandatory_attrs):
            return self.missing_mandatory_attrs[0]
        else:
            return None

    

