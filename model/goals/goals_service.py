from typing import List, TYPE_CHECKING

from pydiet import persistence, goals

if TYPE_CHECKING:
    from pydiet.goals.day_goals import DayGoals


def load_day_goals(datafile_name: str) -> 'DayGoals':
    # Load the data from the datafile;
    dg_data = repository.repository_service.read_day_goals_data(datafile_name)
    # Return the dg instance;
    return goals.day_goals.DayGoals(dg_data)


def load_new_day_goals() -> 'DayGoals':
    # Load the blank data;
    data = goals.day_goals.DATA_TEMPLATE
    # Instantiate and return;
    return goals.day_goals.DayGoals(data)


def save_new_day_goals(day_goals: 'DayGoals') -> str:
    return repository.repository_service.create_day_goals_data(day_goals._data)


def update_existing_day_goals(day_goals: 'DayGoals', datafile_name: str) -> None:
    repository.repository_service.update_day_goals_data(day_goals._data, datafile_name)


def convert_day_goals_name_to_datafile_name(day_goals_name: str) -> str:
    # Load the index;
    index = repository.repository_service.read_day_goals_index()
    # Iterate through the index, searching for the filename;
    for datafile_name in index.keys():
        if index[datafile_name] == day_goals_name:
            # Return the corresponding datafile name;
            return datafile_name
    # Raise an exception if none was found
    raise repository.exceptions.NameNotFoundError
