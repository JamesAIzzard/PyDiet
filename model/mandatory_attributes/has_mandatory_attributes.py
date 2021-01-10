import abc
from typing import List, Optional


class HasMandatoryAttributes(abc.ABC):
    """ABC for mandatory attribute functionalitly."""

    def __init__(self, **kwds):
        super.__init__(**kwds)

    @property
    @abc.abstractmethod
    def missing_mandatory_attrs(self) -> List[str]:
        """Returns a list of currently undefined mandatory attributes for the instance."""
        raise NotImplementedError

    @property
    def defined(self) -> bool:
        """Returns True/False to indicate if the instance has any missing mandatory attributes."""
        return len(self.missing_mandatory_attrs) == 0

    @property
    def definition_status_summary(self) -> str:
        """Returns a readable summary of the instance's definition status."""
        if self.defined:
            return 'Complete'
        else:
            return 'Incomplete, needs {}'.format(self.next_mandatory_attr_required)

    @property
    def next_mandatory_attr_required(self) -> Optional[str]:
        """Returns the name of the next mandatory attribute requiring definition."""
        if len(self.missing_mandatory_attrs):
            return self.missing_mandatory_attrs[0]
        else:
            return None
