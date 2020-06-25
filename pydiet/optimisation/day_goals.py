from typing import Dict, TYPE_CHECKING

from pydiet.optimisation import meal_goals

if TYPE_CHECKING:
    from pydiet.optimisation.meal_goals import MealGoals

data_template = {
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
        # Populate the list of meal goal objects;
        self._meal_goals: Dict[str, 'MealGoals'] = {}
        for mg_name in self._data['meal_goals'].keys():
            self._meal_goals[mg_name] = meal_goals.MealGoals(mg_name, self)

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

    @property
    def meal_goals(self) -> Dict[str, 'MealGoals']:
        return self._meal_goals
