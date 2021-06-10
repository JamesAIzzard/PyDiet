"""Defines exceptions for the persistence module."""

import persistence
import exceptions


class BasePersistenceError(exceptions.PyDietError):
    """Base error for the persistence module."""

    def __init__(self, subject: 'persistence.SupportsPersistence' = None):
        self.subject = subject


class UndefinedUniqueValueError(BasePersistenceError):
    """Indicates the unique value is not defined on the instance."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class DatafileNameUndefinedError(BasePersistenceError):
    """Indicates the datafile name is not defined on the instance."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UniqueValueDuplicatedError(BasePersistenceError):
    """Indicates the unique value on the instance is not unique."""

    def __init__(self, duplicated_value: str, **kwargs):
        super().__init__(**kwargs)
        self.duplicated_value = duplicated_value


class DatafileNotFoundError(BasePersistenceError):
    """Indicates the datafile was not found."""

    def __init__(self, missing_datafile_name: str, **kwargs):
        super().__init__(**kwargs)
        self.missing_datafile_name = missing_datafile_name


class UniqueValueNotFoundError(BasePersistenceError):
    """Indicates the unique value was not found in the index."""

    def __init__(self, missing_unique_value: str, **kwargs):
        super().__init__(**kwargs)
        self.missing_unique_value = missing_unique_value
