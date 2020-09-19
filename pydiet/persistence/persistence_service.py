import json
import os
import uuid
from typing import Dict, TypeVar, TYPE_CHECKING, cast, Type, Optional

from pydiet import persistence

if TYPE_CHECKING:
    from pydiet.persistence.supports_persistence import SupportsPersistence

T = TypeVar('T')


def save(subject: 'SupportsPersistence') -> None:
    """Saves the subject.
    Args:
        subject: An instance of SupportsPersistence.
    Raises:
        persistence.exceptions.UniqueFieldUndefinedError
    """
    # Check the unique field is filled in;
    if not subject.unique_field_defined:
        raise persistence.exceptions.UniqueFieldUndefinedError
    # Update or create;
    if subject.datafile_exists:
        _update_datafile(subject)
    elif not subject.datafile_exists:
        _create_datafile(subject)


def count_saved_instances(cls: Type['SupportsPersistence']) -> int:
    """Counts the number of saved instances of the class in the database (by counting entries in the index).
    Args:
        cls: A subclass of SupportsPersistence
    Returns:
        The number of saved instances of the class.
    """
    index_data = _read_index(cls)
    return len(index_data)


def check_unique_val_avail(cls: Type['SupportsPersistence'], ingore_df: Optional[str], proposed_unique_val) -> bool:
    """Checks if the proposed unique value is available for the persistable class type.
    Args:
        cls: A subclass of SupportsPersistence
        ingore_df: Datafile name to be excluded when searching for collisions.
        proposed_unique_val: Propsed unique value.
    Returns:
        True/False to indicate the value's availablilty.
    """
    # Read the index for the persistable class;
    index_data = _read_index(cls)
    # Pop current file if saved;
    if ingore_df is not None:
        index_data.pop(ingore_df)
    # Return answer
    return proposed_unique_val not in index_data.values()


def read_datafile(filepath: str, data_type: Type[T]) -> T:
    """Reads the data from the specified path and returns it as data of the specified type.
    Returns:
        Data of the specified type (e.g 'IngredientData' etc.)
    """
    # Read the datafile contents;
    with open(filepath, 'r') as fh:
        raw_data = fh.read()
        # Parse into dict;
        data = json.loads(raw_data)
        # Return it;
        return cast(data_type, data)


def delete_datafile(subject: 'SupportsPersistence') -> None:
    """Deletes the subject's entry from its index file and then deletes its datafile from disk.
    Args:
        subject: An instance of SupportsPersistance.
    """
    # Delete the subject's entry from its index;
    _delete_index_entry(subject)
    # Delete the datafile from disk;
    os.remove(subject.datafile_path)


def _create_index_entry(subject: 'SupportsPersistence') -> None:
    """Adds an index entry for the subject. Raises an exception if the unique value is not unique in the index.
    Args:
        subject: An instance of SupportsPersistance.
    Raises:
        persistence.exceptions.UniqueValueDuplicatedError
    """
    # Read the index;
    index_data = _read_index(subject.__class__)
    # Check the unique field value isn't used already;
    if not check_unique_val_avail(subject.__class__, subject.datafile_name, subject.unique_field_value):
        raise persistence.exceptions.UniqueValueDuplicatedError
    # Generate and set the UID on object and index;
    subject.set_datafile_name(str(uuid.uuid4()))
    index_data[cast(str, subject.datafile_name)] = cast(
        str, subject.unique_field_value)
    # Write the index;
    with open(subject.get_index_filepath(), 'w') as fh:
        json.dump(index_data, fh, indent=2, sort_keys=True)


def _create_datafile(subject: 'SupportsPersistence') -> None:
    """Inserts the subjects unique field into the index against a new datafile name, and then writes the objects data
    in a new datafile on the disk.
    Args:
        subject: An instance of SupportsPersistance.
    """
    # Create the index entry;
    _create_index_entry(subject)
    # Create the datafile;
    with open(subject.datafile_path, 'w') as fh:
        json.dump(subject.data_copy, fh, indent=2, sort_keys=True)


def _read_index(cls: Type['SupportsPersistence']) -> Dict[str, str]:
    """Returns the index corresponding to the subject.
    Args:
        cls: A subclass of SupportsPersistance.
    Returns:
        The index associated with cls.
    """
    with open(cls.get_index_filepath(), 'r') as fh:
        raw_data = fh.read()
        return json.loads(raw_data)


def _update_datafile(subject: 'SupportsPersistence') -> None:
    """Updates the subject's index (to catch any changes to the unique field value), and overwrites the old datafile on
    disk with the current data.
    Args:
        subject: An instance of SupportsPersistence.
    """
    # Update the index;
    _update_index_entry(subject)
    # Update the datafile;
    with open(subject.datafile_path, 'w') as fh:
        json.dump(subject.data_copy, fh, indent=2, sort_keys=True)


def _update_index_entry(subject: 'SupportsPersistence') -> None:
    """Updates the index saved to disk with the latestingr unique field value on the object. Raises an exception if the
    unique value is not unique in the index.
    Args:
        subject: An instance of SupportsPersistence.
    Raises:
        persistence.exceptions.UniqueFieldDuplicatedError
    """
    # Read the index;
    index_data = _read_index(subject.__class__)
    # Pop the filename so we don't detect a name clash if it hasn't changed;
    index_data.pop(cast(str, subject.datafile_name))
    # Check the unique field value isn't used already;
    if subject.unique_field_value in index_data.values():
        raise persistence.exceptions.UniqueValueDuplicatedError
    # Update the index;
    index_data[cast(str, subject.datafile_name)] = cast(str, subject.unique_field_value)
    with open(subject.__class__.get_index_filepath(), 'w') as fh:
        json.dump(index_data, fh, indent=2, sort_keys=True)


def _delete_index_entry(subject: 'SupportsPersistence') -> None:
    """Deletes the subject's entry from its index.
    Args:
        subject: An instance of SupportsPersistence.
    """
    # Read the index;
    index_data = _read_index(subject.__class__)
    # Remove the key/value from the index;
    del index_data[cast(str, subject.datafile_name)]
    with open(subject.__class__.get_index_filepath(), 'w') as fh:
        json.dump(index_data, fh, indent=2, sort_keys=True)
