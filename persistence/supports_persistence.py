import abc
from typing import Dict, Any, Optional

import persistence


class SupportsPersistence(abc.ABC):
    """ABC for object persistence functionality."""

    def __init__(self, unique_value: Optional[str] = None, datafile_name: Optional[str] = None, **kwds):
        super().__init__(**kwds)
        self._unique_value = unique_value
        self._datafile_name: Optional[str] = datafile_name

    @staticmethod
    @abc.abstractmethod
    def get_path_into_db() -> str:
        """Returns the path into the class' database."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def persistable_data(self) -> Dict[str, Any]:
        """Returns the persistable data for this instance."""
        raise NotImplementedError

    @abc.abstractmethod
    def load_data(self, data: Dict[str, Any]) -> None:
        """Loads saved data into the instance."""
        raise NotImplementedError

    @property
    def unique_value_defined(self) -> bool:
        """Returns True/False to indicate if the unique value is defined."""
        return self._unique_value is not None

    @property
    def unique_value(self) -> str:
        """Returns the unique value."""
        return self._unique_value

    @unique_value.setter
    def unique_value(self, value: str) -> None:
        """Sets the unique value while ensuring the value being set is unique to that class.
        Raises:
            NameDuplicatedError: To indicate there is another saved instance of this class
                with the same name.
        """
        # Only things that can be expressed as strings can be unique values;
        value = str(value)
        # Set the value if it isn't taken already;
        if persistence.check_unique_value_available(self.__class__, value, self.datafile_name):
            self._unique_value = value
        else:
            raise persistence.exceptions.UniqueValueDuplicatedError

    @property
    def datafile_name(self) -> Optional[str]:
        """Returns the datafile name for the instance."""
        return self._datafile_name

    @property
    def has_unsaved_changes(self) -> bool:
        """Indicates if the persistable data has changed since previous save."""
        # Definately has unsaved changes if it hasn't been saved yet.
        if not self.datafile_exists:
            return True
        # Otherwise, compare the current data with the saved data.
        saved_version = persistence.load(self.__class__, self.datafile_name)
        return self.persistable_data == saved_version.persistable_data

    @property
    def datafile_exists(self) -> bool:
        """Returns True/False to indicate if the instance has been previously saved."""
        return self._datafile_name is not None

    @classmethod
    def get_index_filepath(cls) -> str:
        """Returns the class' index filepath."""
        return '{}index.json'.format(cls.get_path_into_db())

    @property
    def datafile_path(self) -> str:
        """Returns the entire path to the instance's datafile."""
        if not self.datafile_exists:
            raise persistence.exceptions.DatafileNotFoundError
        else:
            return self.get_path_into_db() + self.datafile_name + '.json'
