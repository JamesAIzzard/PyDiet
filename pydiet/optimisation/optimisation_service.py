from typing import List, TYPE_CHECKING

from pydiet import repository_service as rps
from pydiet.optimisation import day_goals
from pydiet.optimisation.exceptions import (
    DayGoalsNotFoundError
)

if TYPE_CHECKING:
    from pydiet.optimisation.day_goals import DayGoals


def load_day_goals(datafile_name: str) -> 'DayGoals':
    dg_data = rps.read_day_goals_data(datafile_name)
    return day_goals.DayGoals(dg_data)


def load_new_day_goals() -> 'DayGoals':
    # Load the blank data;
    data = day_goals.data_template
    # Instantiate and return;
    return day_goals.DayGoals(data)


def save_new_day_goals(day_goals: 'DayGoals') -> str:
    return rps.create_day_goals_data(day_goals._data)


def update_existing_day_goals(day_goals: 'DayGoals', datafile_name: str) -> None:
    rps.update_day_goals_data(day_goals._data, datafile_name)


def convert_day_goals_name_to_datafile_name(day_goals_name: str) -> str:
    # Load the index;
    index = rps.read_day_goals_index()
    # Iterate through the index, searching for the filename;
    for datafile_name in index.keys():
        if index[datafile_name] == day_goals_name:
            # Return the corresponding datafile name;
            return datafile_name
    # Raise an exception if none was found
    raise DayGoalsNotFoundError
