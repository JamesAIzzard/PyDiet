from typing import Dict

_day_goal_data_template = {
    "solution_datafile_names": {},
    "max_cost_gbp": None,
    "flags": [],
    "total_cals": None,
    "total_perc_fat": None,
    "total_perc_carbs": None,
    "total_perc_protein": None,
    "nutrient_mass_targets": {},
    "meal_goals": {}
}


class DayGoals():
    def __init__(self, data: Dict):
        self._data = data

    @property
    def name(self) -> str:
        return self._data['name']

    @name.setter
    def name(self, value: str) -> None:
        self._data['name'] = value

    @property
    def max_cost_gbp(self) -> float:
        return self._data['max_cost_gbp']

    @max_cost_gbp.setter
    def max_cost_gbp(self, value: float) -> None:
        self._data['max_cost_gbp'] = value
