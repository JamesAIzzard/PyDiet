import abc
from typing import Dict, Optional

from pydiet import persistence, HasSettableName
from pydiet.persistence import exceptions


class SupportsPersistence(HasSettableName, abc.ABC):
    """ABC for object persistence functionality."""

    def __init__(self, datafile_name: Optional[str] = None, **kwds):
        super().__init__(**kwds)
        self._datafile_name: Optional[str] = datafile_name

    @staticmethod
    @abc.abstractmethod
    def get_path_into_db() -> str:
        """Returns the path into the class' database."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def persistable_data(self) -> 'Dict':
        """Returns the persistable data for this instance."""
        raise NotImplementedError

    @property
    def datafile_name(self) -> Optional[str]:
        """Returns the datafile name for the instance."""
        return self._datafile_name

    def _set_name(self, name: str) -> None:
        """Modifies the name setter to ensure the name being set is unique to that class.
        Raises:
            NameDuplicatedError: To indicate there is another saved instance of this class
                with the same name.
        """
        if persistence.check_name_available(self.__class__, name, self.datafile_name):
            self._name = name
        else:
            raise exceptions.NameDuplicatedError

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
        return self._datafile_name is None

    @classmethod
    def get_index_filepath(cls) -> str:
        """Returns the class' index filepath."""
        return '{}index.json'.format(cls.get_path_into_db())

    @property
    def datafile_path(self) -> str:
        """Returns the entire path to the instance's datafile."""
        if not self.datafile_exists:
            raise persistence.exceptions.NoDatafileError
        else:
            return self.get_path_into_db() + self.datafile_name + '.json'
