import json
import os
import uuid
from typing import Dict, List, Any, TypeVar, Type, Optional, Union, TYPE_CHECKING

from . import exceptions

if TYPE_CHECKING:
    from pydiet.persistence.supports_persistence import SupportsPersistence

T = TypeVar('T')


def save(subject: 'SupportsPersistence') -> None:
    """Saves the subject."""

    # Check the name is filled in and available;
    if not subject.name_is_defined:
        raise exceptions.NameUndefinedError
    if check_name_available(subject.__class__, subject.name, subject.datafile_name) is False:
        raise exceptions.NameDuplicatedError

    # If exists already, we are updating;
    if subject.datafile_exists:
        _update_datafile(subject)
    # Otherwise, save in a new datafile;
    else:
        _create_datafile(subject)


def load(cls: Union[Type[T], 'SupportsPersistence'], name: Optional[str] = None,
         datafile_name: Optional[str] = None) -> T:
    """Loads and returns an instance of the specified type, corresponding to the
    unique field name provided."""

    # Check the params are OK and get the datafile name if required;
    if name is None and datafile_name is None:
        raise ValueError('Either name or datafile name must be provided.')
    if name is not None:
        datafile_name = _get_datafile_name_for_name(cls, name)

    # Load & return;
    datafile = _read_datafile(cls.get_path_into_db() + datafile_name + '.json')
    loaded_instance = cls(name=name, datafile_name=datafile_name, datafile=datafile)
    return loaded_instance


def delete(cls: Type['SupportsPersistence'], name: Optional[str] = None,
           datafile_name: Optional[str] = None) -> None:
    """Deletes the instance of the specified type, with the specified unique value, from the database."""

    # Check the params are OK and get the datafile name if required;
    if name is None and datafile_name is None:
        raise ValueError('Either name or datafile name must be provided.')
    if name is not None:
        datafile_name = _get_datafile_name_for_name(cls, name)

    # Delete;
    _delete_index_entry(cls, datafile_name)
    _delete_datafile(cls, datafile_name)


def count_saved_instances(cls: Type['SupportsPersistence']) -> int:
    """Counts the number of saved instances of the class in the database (by counting entries in the index)."""
    index_data = _read_index(cls)
    return len(index_data)


def get_saved_names(cls: Type['SupportsPersistence']) -> List[str]:
    """Returns a list of all persisted unique names. For example: If the class
    is Ingredient, this would return all saved ingredient names."""
    index = _read_index(cls)
    return list(index.values())


def check_name_available(cls: Type['SupportsPersistence'], proposed_name: str,
                         ingore_datafile: Optional[str] = None) -> bool:
    """Checks if the proposed unique value is available for the persistable class type."""

    if proposed_name is None:
        raise exceptions.NameUndefinedError

    index_data = _read_index(cls)

    if ingore_datafile is not None:
        index_data.pop(ingore_datafile)

    return proposed_name not in index_data.values()


def _get_datafile_name_for_name(cls: Type['SupportsPersistence'], name: str) -> str:
    """Returns the datafile name associated with the unique name."""
    index = _read_index(cls)
    for df_name, u_name in index.items():
        if u_name == name:
            return df_name
    raise exceptions.NoDatafileError


def _create_index_entry(subject: 'SupportsPersistence') -> None:
    """Adds an index entry for the subject, setting its datafile_name field in the process.
    Raises:
         NameDuplicatedError: To indicate the unique value is not unique in the index.
    """
    index_data = _read_index(subject.__class__)

    # Check the unique field value isn't used already, also checks name is not None;
    if not check_name_available(subject.__class__, subject.name, subject.datafile_name):
        raise exceptions.NameDuplicatedError

    # Generate and set the UID on object and index;
    subject._datafile_name = str(uuid.uuid4())
    index_data[subject.datafile_name] = subject.name

    # Write the index;
    with open(subject.get_index_filepath(), 'w') as fh:
        json.dump(index_data, fh, indent=2, sort_keys=True)


def _create_datafile(subject: 'SupportsPersistence') -> None:
    """Adds the subject details to its index and writes its datafile."""
    # Create the index entry;
    _create_index_entry(subject)
    # Create the datafile;
    with open(subject.datafile_path, 'w') as fh:
        json.dump(subject.persistable_data, fh, indent=2, sort_keys=True)


def _read_datafile(filepath: str) -> Dict[str, Any]:
    """Returns the data in the specified file as json."""
    with open(filepath, 'r') as fh:
        raw_data = fh.read()
        return json.loads(raw_data)


def _read_index(cls: Type['SupportsPersistence']) -> Dict[str, str]:
    """Returns the index corresponding to the _subject."""
    with open(cls.get_index_filepath(), 'r') as fh:
        raw_data = fh.read()
        return json.loads(raw_data)


def _update_datafile(subject: 'SupportsPersistence') -> None:
    """Updates the subject's index (to catch any changes to the name), and overwrites the
    old datafile on disk with the current data."""

    # Update the index;
    _updated_indexed_name(subject)

    # Update the datafile;
    with open(subject.datafile_path, 'w') as fh:
        json.dump(subject.persistable_data, fh, indent=2, sort_keys=True)


def _updated_indexed_name(subject: 'SupportsPersistence') -> None:
    """Updates the index saved to disk with the current name on the instance.
    Raises:
        NameDuplicatedError: To indicate the name is not unique.
    """

    # Check the name is unique;
    if not check_name_available(subject.__class__, subject.name, subject.datafile_name):
        raise exceptions.NameDuplicatedError

    # Do the update;
    index_data = _read_index(subject.__class__)
    index_data[subject.datafile_name] = subject.name
    with open(subject.__class__.get_index_filepath(), 'w') as fh:
        json.dump(index_data, fh, indent=2, sort_keys=True)


def _delete_index_entry(cls: Type['SupportsPersistence'], datafile_name: str) -> None:
    """Deletes the _subject's entry from its index."""
    index_data = _read_index(cls)
    del index_data[datafile_name]
    with open(cls.get_index_filepath(), 'w') as fh:
        json.dump(index_data, fh, indent=2, sort_keys=True)


def _delete_datafile(cls: Type['SupportsPersistence'], datafile_name: str) -> None:
    """Deletes the specified datafile from the specified type's database."""
    os.remove(cls.get_path_into_db() + datafile_name + '.json')
