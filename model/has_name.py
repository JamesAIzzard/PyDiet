"""Defines functionality required to model named instances."""
import abc
from typing import Optional, Dict, Any

import persistence
import model


class HasName(persistence.YieldsPersistableData):
    """Abstract class to define readonly name functionality."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    @abc.abstractmethod
    def _name(self) -> Optional[str]:
        """Returns the name if defined, None if not."""
        raise NotImplementedError

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

    @property
    def persistable_data(self) -> Dict[str, Any]:
        """Returns instance's persistable data."""
        data = super().persistable_data
        data['name'] = self.name
        return data


class HasSettableName(HasName, persistence.CanLoadData):
    """Abstract class to define writeable name functionality."""

    def __init__(self, name: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)

        self._name_ = name

    @property
    def _name(self) -> Optional[str]:
        """Returns the locally stored name."""
        return self._name_

    @HasName.name.setter
    def name(self, name: Optional[str]) -> None:
        """Gets the instance's name."""
        self._name_ = name

    def load_data(self, data: Dict[str, Any]) -> None:
        """Loads instance data."""
        # Load the data on the superclass;
        super().load_data(data)

        # If we don't have any data in this dict, just return;
        if 'name' not in data.keys():
            return

        # OK, we do have data, so load it;
        self._name_ = data['name']
