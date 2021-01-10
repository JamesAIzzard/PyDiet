import abc
from typing import Optional

from . import exceptions


class HasName(abc.ABC):
    """Models any object with a name."""

    def __init__(self, name: Optional[str] = None, **kwds):
        self._name: Optional[str] = None

        if name is not None:
            self.name = name

    @property
    def name(self) -> Optional[str]:
        """Returns the object's name."""
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Sets the object's name."""
        self._set_name(name)

    def _set_name(self, name: str) -> None:
        """Internal method to allow subclasses to configure the set_name behaviour."""
        raise exceptions.NameNotSettableError

    @property
    def name_is_defined(self) -> bool:
        """Returns True/False to indicate if the object's name is defined."""
        if self.name is None:
            return False
        else:
            return True

    @property
    def name_summary(self) -> str:
        """Returns a summary of the object's name."""
        if self.name_is_defined:
            return self.name
        else:
            return 'Undefined'


class HasSettableName(HasName, abc.ABC):
    """Models any object with a settable name."""

    def __init__(self, **kwds):
        super().__init__(**kwds)

    def _set_name(self, name: Optional[str]) -> None:
        self._name = name
