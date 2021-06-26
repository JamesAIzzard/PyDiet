"""Data persistence functionality."""
import json
import os
import uuid
from difflib import SequenceMatcher
from heapq import nlargest
from typing import Dict, List, Any, TypeVar, Type, Optional

import persistence

T = TypeVar('T')


class Cache:
    """Data cache class."""

    def __init__(self):
        self.datafiles: Dict[str, Dict] = {}
        self.indexes: Dict[str, Dict] = {}
        self.recipe_precalc_data: Dict[str, Dict] = {}
        self.recipes_by_tag: Dict[str, str] = {}

    def reset(self):
        """Reset all caches to empty."""
        self.datafiles = {}
        self.indexes = {}
        self.recipe_precalc_data = {}
        self.recipes_by_tag = {}


cache = Cache()


def get_recipe_df_names_by_tag(tag:str) -> List[str]:
    """Returns a list of recipe datafile names corresponding to the specified tag."""
    if cache.recipes_by_tag == {}:
        cache.recipes_by_tag = _read_datafile(f"{persistence.configs.PATH_INTO_DB}/precalc_data/recipes_by_tag.json")
    return cache.recipes_by_tag[tag]


def get_precalc_data_for_recipe(datafile_name: str) -> Dict[str, Any]:
    """Gets the precalc data for the named recipe."""
    if cache.recipe_precalc_data == {}:
        cache.recipe_precalc_data = _read_datafile(f"{persistence.configs.PATH_INTO_DB}/precalc_data/recipes.json")
    return cache.recipe_precalc_data[datafile_name]


def save_instance(subject: 'persistence.SupportsPersistence') -> None:
    """Saves the subject."""

    # Check the name is available;
    if check_unique_value_available(
            cls=subject.__class__,
            proposed_value=subject.unique_value,
            ignore_datafile=subject.datafile_name if subject.datafile_name_is_defined else None
    ) is False:
        raise persistence.exceptions.UniqueValueDuplicatedError(
            subject.unique_value
        )

    # If exists already, we are updating;
    if subject.datafile_name_is_defined:
        _update_datafile(subject)
    # Otherwise, save in a new datafile;
    else:
        _create_datafile(subject)


def load_instance(cls: Type[T], unique_value: Optional[str] = None,
                  datafile_name: Optional[str] = None) -> T:
    """Loads and returns an instance of the specified type, corresponding to the
    unique field name provided."""
    # Load & return;
    data = load_datafile(cls=cls, unique_value=unique_value, datafile_name=datafile_name)
    loaded_instance = cls(datafile_name=datafile_name)
    loaded_instance.load_data(data)
    return loaded_instance


def load_datafile(cls: Any, unique_value: Optional[str] = None, datafile_name: Optional[str] = None) -> Dict[str, Any]:
    """Returns the datafile for the specified instance."""
    # Check the params are OK and get the datafile name if required;
    if unique_value is None and datafile_name is None:
        raise ValueError('Either name or datafile name must be provided.')
    if unique_value is not None:
        datafile_name = get_datafile_name_for_unique_value(cls, unique_value)

    if datafile_name not in cache.datafiles.keys():
        cache.datafiles[datafile_name] = _read_datafile(f"{cls.get_path_into_db()}/{datafile_name}.json")

    # Load and return;
    return cache.datafiles[datafile_name]


def delete_instances(cls: Type['persistence.SupportsPersistence'], name: Optional[str] = None,
                     datafile_name: Optional[str] = None) -> None:
    """Deletes the instance of the specified type, with the specified unique qty, from the database."""

    # Check the params are OK and get the datafile name if required;
    if name is None and datafile_name is None:
        raise ValueError('Either name or datafile name must be provided.')
    if name is not None:
        datafile_name = get_datafile_name_for_unique_value(cls, name)

    # Delete;
    _delete_index_entry(cls, datafile_name)
    _delete_datafile(cls, datafile_name)


def count_saved_instances(cls: Type['persistence.SupportsPersistence']) -> int:
    """Counts the number of saved instances of the class in the database (by counting entries in the index)."""
    index_data = read_index(cls)
    return len(index_data)


def get_saved_unique_values(cls: Type['persistence.SupportsPersistence']) -> List[str]:
    """Returns a list of all persisted unique values. For example: If the class
    is Ingredient, this would return all saved ingredient names."""
    index = read_index(cls)
    return list(index.values())


def check_unique_value_available(cls: Type['persistence.SupportsPersistence'], proposed_value: str,
                                 ignore_datafile: Optional[str] = None) -> bool:
    """Checks if the proposed unique value is available for the persistable class type."""

    # Check proposed name was provided;
    if proposed_value is None:
        raise persistence.exceptions.UndefinedUniqueValueError

    # Grab the index data;
    index_data = read_index(cls)

    # If we are ignoring a datafile, remove it from the index data;
    if ignore_datafile is not None:
        index_data.pop(ignore_datafile)

    return proposed_value not in index_data.values()


def search_for_unique_values(
        subject_type: Type['persistence.SupportsPersistence'],
        search_name: str,
        num_results: int = 5) -> List[str]:
    """Returns a list of n unique values which match the search term most closely."""

    def score_similarity(words_to_score: List[str], search_term: str) -> Dict[str, float]:
        """Return a dict with numerical values associated with each word, to indicate similarity to the
        search term."""
        scores = {}
        for word in words_to_score:
            scores[word] = SequenceMatcher(None, search_term, word).ratio()
        return scores

    all_names = get_saved_unique_values(subject_type)
    all_scores = score_similarity(all_names, search_name)
    return nlargest(num_results, all_scores, key=all_scores.get)


def get_datafile_name_for_unique_value(cls: Type['persistence.SupportsPersistence'], unique_value: str) -> str:
    """Returns the datafile name associated with the unique name."""
    index = read_index(cls)
    for df_name, u_name in index.items():
        if u_name.strip() == unique_value.strip():
            return df_name
    raise persistence.exceptions.UniqueValueNotFoundError(missing_unique_value=unique_value)


def get_unique_value_from_datafile_name(cls: Type['persistence.SupportsPersistence'], datafile_name: str) -> str:
    """Returns the unique value associated with the datafile name."""
    index = read_index(cls)
    for df_name, u_name in index.items():
        if datafile_name == df_name:
            return u_name
    raise persistence.exceptions.DatafileNotFoundError(
        missing_datafile_name=datafile_name
    )


def _create_index_entry(subject: 'persistence.SupportsPersistence') -> None:
    """Adds an index entry for the subject, setting its datafile_name field in the process.
    Raises:
         NameDuplicatedError: To indicate the unique qty is not unique in the index.
    """
    index_data = read_index(subject.__class__)

    # Check the unique field qty isn't used already, also checks name is not None;
    if not check_unique_value_available(
            cls=subject.__class__,
            proposed_value=subject.unique_value,
            ignore_datafile=subject.datafile_name if subject.datafile_name_is_defined else None
    ):
        raise persistence.exceptions.UniqueValueDuplicatedError

    # Generate and set the UID on object and index;
    subject._datafile_name = str(uuid.uuid4())
    index_data[subject.datafile_name] = subject.unique_value

    # Write the index;
    with open(subject.get_index_filepath(), 'w') as fh:
        json.dump(index_data, fh, indent=2, sort_keys=True)


def _create_datafile(subject: 'persistence.SupportsPersistence') -> None:
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


def read_index(cls: Type['persistence.SupportsPersistence']) -> Dict[str, str]:
    """Returns the index corresponding to the _subject."""
    if cls.__name__ in cache.indexes:
        return cache.indexes[cls.__name__]
    with open(cls.get_index_filepath(), 'r') as fh:
        raw_data = fh.read()
        cache.indexes[cls.__name__] = json.loads(raw_data)
        return cache.indexes[cls.__name__]


def _update_datafile(subject: 'persistence.SupportsPersistence') -> None:
    """Updates the subject's index (to catch any changes to the name), and overwrites the
    old datafile on disk with the current data."""

    # Update the index;
    _update_unique_value(subject)

    # Update the datafile;
    with open(subject.datafile_path, 'w') as fh:
        json.dump(subject.persistable_data, fh, indent=2, sort_keys=True)


def _update_unique_value(subject: 'persistence.SupportsPersistence') -> None:
    """Updates the index saved to disk with the current name on the instance.
    Raises:
        NameDuplicatedError: To indicate the name is not unique.
    """

    # Check the name is unique;
    if not check_unique_value_available(subject.__class__, subject.unique_value, subject.datafile_name):
        raise persistence.exceptions.UniqueValueDuplicatedError

    # Do the update;
    index_data = read_index(subject.__class__)
    index_data[subject.datafile_name] = subject.unique_value
    with open(subject.__class__.get_index_filepath(), 'w') as fh:
        json.dump(index_data, fh, indent=2, sort_keys=True)


def _delete_index_entry(cls: Type['persistence.SupportsPersistence'], datafile_name: str) -> None:
    """Deletes the subject's entry from its index."""
    index_data = read_index(cls)
    del index_data[datafile_name]
    with open(cls.get_index_filepath(), 'w') as fh:
        json.dump(index_data, fh, indent=2, sort_keys=True)


def _delete_datafile(cls: Type['persistence.SupportsPersistence'], datafile_name: str) -> None:
    """Deletes the specified datafile from the specified type's database."""
    os.remove(cls.get_path_into_db() + datafile_name + '.json')
