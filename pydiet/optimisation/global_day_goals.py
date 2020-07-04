from singleton_decorator import singleton

from pydiet import repository_service as rps

@singleton
class GlobalDayGoals():
    def __init__(self):
        self._data = rps.read_global_day_goals_data()

    @property
    def max_cost_gbp(self) -> float:
        raise NotImplementedError