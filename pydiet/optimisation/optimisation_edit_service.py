from typing import Optional, TYPE_CHECKING

from singleton_decorator import singleton

import pydiet
from pydiet.optimisation import optimisation_service as ops

if TYPE_CHECKING:
    from pydiet.optimisation.day_goals import DayGoals

@singleton
class OptimisationEditService():
    def __init__(self):
        self.day_goals: Optional['DayGoals'] = None
        self.datafile_name: Optional[str] = None

    def save_changes(self):
        # Check there is a daygoals instance loaded;
        if not self.day_goals:
            raise AttributeError
        # If we are creating the daygoals for the first time;
        if not self.datafile_name:
            # Create the new datafile and stash the name;
            self.datafile_name = ops.save_new_day_goals(self.day_goals)
            pydiet.app.info_message = 'Day goals saved.'
            return
        # If we are updating an existing datafile;
        else:
            ops.update_existing_day_goals(
                self.day_goals,
                self.datafile_name
            )
            pydiet.app.info_message = 'Day goals saved.'
            return