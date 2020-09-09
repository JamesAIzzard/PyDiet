import abc

from typing import TypedDict, Union, Dict, Optional, cast

from pydiet import persistence


class PersistenceInfo(TypedDict):
    data: Union[TypedDict, Dict]
    datafile_name: Optional[str]

class DBInfo(TypedDict):
    unique_field_name: str
    path_into_db: str

class SupportsPersistence(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def get_db_info() -> 'DBInfo':
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def readonly_persistence_info(self) -> 'PersistenceInfo':
        raise NotImplementedError

    @abc.abstractmethod
    def set_datafile_name(self, datafile_name: str) -> None:
        raise NotImplementedError

    @property
    def datafile_exists(self) -> bool:
        if self.readonly_persistence_info['datafile_name'] == None:
            return False
        else:
            return True

    @classmethod
    def get_unique_field_name(cls) -> str:
        return cls.get_db_info()['unique_field_name']

    @property
    def unique_field_value(self) -> Optional[str]:
        return cast(Optional[str], self.readonly_persistence_info['data']
                    [self.get_unique_field_name()])

    @classmethod
    def get_path_into_db(cls) -> str:
        return cls.get_db_info()['path_into_db']

    @classmethod
    def get_index_filepath(cls) -> str:
        return '{}{}.json'.format(cls.get_path_into_db(), persistence.configs.indexes_filename)

    @property
    def datafile_name(self) -> Optional[str]:
        return cast(Optional[str], self.readonly_persistence_info['datafile_name'])

    @property
    def datafile_path(self) -> str:
        if not self.datafile_exists:
            raise persistence.exceptions.NoDatafileError
        else:
            return '{path_to_db_dir}{datafile_name}.json'.format(
                path_to_db_dir=self.get_path_into_db(),
                datafile_name=self.datafile_name)

    @property
    def data(self) -> Union[Dict, TypedDict]:
        return self.readonly_persistence_info['data']
