"""Functionality related to classes which support persistance."""
import abc
from typing import Dict, Any, Optional

import persistence


class YieldsPersistableData(abc.ABC):
    """Base class for objects that can output persistable data."""

    @property
    @abc.abstractmethod
    def persistable_data(self) -> Dict[str, Any]:
        """Returns the persistable data for this instance."""
        # Just the base class here, so just return an empty dict;
        return {}


class CanLoadData(abc.ABC):
    """Base class for objects that can load persistable data."""

    @abc.abstractmethod
    def load_data(self, data: Dict[str, Any]) -> None:
        """Loads the classes persistable data type into the object."""
        pass


class SupportsPersistence(YieldsPersistableData, abc.ABC):
    """ABC for object persistence functionality."""

    def __init__(self, datafile_name: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)

        self._datafile_name: Optional[str] = datafile_name

    @staticmethod
    @abc.abstractmethod
    def get_path_into_db() -> str:
        """Returns the path into the class' database."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def unique_value(self) -> str:
        """Get the unique value for the instance."""
        raise NotImplementedError

    def validate_unique_value(self, value: str) -> str:
        """Checks the proposed unique value for uniqueness, and returns it if it is unique."""
        if persistence.check_unique_value_available(
                cls=self.__class__,
                proposed_name=value,
                ignore_datafile=self._datafile_name
        ) is True:
            return value
        else:
            raise persistence.exceptions.UniqueValueDuplicatedError(
                subject=self,
                duplicated_value=value
            )

    @property
    def datafile_name(self) -> str:
        """Returns the datafile name for the instance."""
        if self._datafile_name is None:
            raise persistence.exceptions.DatafileNameUndefinedError(subject=self)
        return self._datafile_name

    @property
    def has_unsaved_changes(self) -> bool:
        """Indicates if the persistable data has changed since previous save."""
        # Definately has unsaved changes if it hasn't been saved yet.
        if not self.datafile_name_is_defined:
            return True
        # Otherwise, compare the current data with the saved data.
        saved_version = persistence.load_instance(self.__class__, datafile_name=self.datafile_name)
        return not self.persistable_data == saved_version.persistable_data

    @property
    def datafile_name_is_defined(self) -> bool:
        """Returns True/False to indicate if the instance has been previously saved."""
        return self._datafile_name is not None

    @classmethod
    def get_index_filepath(cls) -> str:
        """Returns the class' index filepath."""
        return f"{cls.get_path_into_db()}/index.json"

    @property
    def datafile_path(self) -> str:
        """Returns the entire path to the instance's datafile."""
        if not self.datafile_name_is_defined:
            raise persistence.exceptions.DatafileNotFoundError
        else:
            return f"{self.get_path_into_db()}/{self.datafile_name}.json"
