"""General use classes for model."""
import abc
from typing import List, Dict, Optional, Any

import model
import persistence


class HasName(persistence.CanLoadData):
    """Abstract class to define readonly name functionality."""

    def __init__(self, name: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)

        # Always stores name locally;
        self._name: Optional[str] = None

        if name is not None:
            self.load_data(data={'name': name})

    @property
    def name(self) -> str:
        """Returns the instance's name.
        Notes:
            The class doesn't say anything about whether the name must be defined or not, so
            its OK to return None if the name is not defined.
        """
        if self._name is None:
            raise model.exceptions.UndefinedNameError(subject=self)
        return self._name

    @property
    def name_is_defined(self) -> bool:
        """Returns True/False to indicate if the name is defined."""
        if self._name is None:
            return False
        else:
            return True

    def load_data(self, data: Dict[str, Any]) -> None:
        """Loads instance data."""
        super().load_data(data)
        self._name = data['name']

    @property
    def persistable_data(self) -> Dict[str, Any]:
        """Returns instance's persistable data."""
        data = super().persistable_data
        data['name'] = self.name
        return data


class HasSettableName(HasName):
    """Abstract class to define writeable name functionality."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @HasName.name.setter
    def name(self, name: Optional[str]) -> None:
        """Gets the instance's name."""
        self._name = name


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
