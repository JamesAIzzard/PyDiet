"""Defines functionality associated with classes that can be defined/undefined."""
import abc
from typing import List, Optional


class SupportsDefinition(abc.ABC):
    """Models functionlity associated with being fully/not fully defined."""

    @property
    @abc.abstractmethod
    def is_defined(self) -> bool:
        """Returns True/False to indicate if the instance is defined."""
        raise NotImplementedError

    @property
    def is_undefined(self) -> bool:
        """Returns True/False to indicate if the instance is undefined."""
        return not self.is_defined


class HasMandatoryAttributes(SupportsDefinition, abc.ABC):
    """ABC for mandatory attribute functionalitly."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    @abc.abstractmethod
    def missing_mandatory_attrs(self) -> List[str]:
        """Returns a list of currently undefined mandatory attributes for the instance."""
        raise NotImplementedError

    @property
    def is_defined(self) -> bool:
        """Returns True/False to indicate if the instance is defined."""
        # We are defined, if the list of mandatory attributes has no items in it.
        return len(self.missing_mandatory_attrs) == 0

    @property
    def definition_status_summary(self) -> str:
        """Returns a readable summary of the instance's definition status."""
        if self.is_defined:
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
