import abc

from typing import TypedDict, Union, Dict, Optional, cast

from pydiet import persistence


class PersistenceInfo(TypedDict):
    data: Union[TypedDict, Dict]
    datafile_name: Optional[str]
    unique_field_name: str
    path_into_db: str


class SupportsPersistence(abc.ABC):

    @property
    @abc.abstractmethod
    def readonly_persistence_data(self) -> 'PersistenceInfo':
        raise NotImplementedError

    @abc.abstractmethod
    def set_datafile_name(self, datafile_name: str) -> None:
        raise NotImplementedError

    def datafile_exists(self) -> bool:
        if self.readonly_persistence_data['datafile_name'] == None:
            return False
        else:
            return True

    @property
    def unique_field_name(self) -> str:
        return self.readonly_persistence_data['unique_field_name']

    @property
    def unique_field_value(self) -> Optional[str]:
        return cast(Optional[str], self.readonly_persistence_data['data']
                    [self.unique_field_name])

    @property
    def path_into_db(self) -> str:
        return self.readonly_persistence_data['path_into_db']

    @property
    def index_filepath(self) -> str:
        return '{}{}.json'.format(self.path_into_db, persistence.configs.indexes_filename)

    @property
    def datafile_name(self) -> str:
        if self.readonly_persistence_data['datafile_name'] == None:
            raise persistence.exceptions.NoDatafileError
        return cast(str, self.readonly_persistence_data['datafile_name'])

    @property
    def datafile_path(self) -> str:
        if not self.datafile_exists:
            raise persistence.exceptions.NoDatafileError
        else:
            return '{path_to_db_dir}{datafile_name}.json'.format(
                path_to_db_dir=self.path_into_db,
                datafile_name=self.datafile_name)

    @property
    def data(self) -> Union[Dict, TypedDict]:
        return self.readonly_persistence_data['data']
