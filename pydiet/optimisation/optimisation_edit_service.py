from typing import Optional, TYPE_CHECKING

from singleton_decorator import singleton

if TYPE_CHECKING:
    from pydiet.optimisation.day_goals import DayGoals

@singleton
class OptimisationEditService():
    def __init__(self):
        self.day_goals: Optional['DayGoals'] = None