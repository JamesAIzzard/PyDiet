from typing import Dict, TYPE_CHECKING

from pydiet.optimisation import meal_goals
from pydiet.optimisation.exceptions import DuplicateMealGoalsNameError

if TYPE_CHECKING:
    from pydiet.optimisation.meal_goals import MealGoals

data_template = {
    "name": None,
    "solution_datafile_names": {},
    "max_cost_gbp": None,
    "flags": [],
    "calories": None,
    "perc_fat": None,
    "perc_carbs": None,
    "perc_protein": None,
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

    def add_meal_goal(self, meal_name: str, meal_goals: 'MealGoals') -> None:
        # Check there isn't a meal by this name already;
        if meal_name in self.meal_goals.keys():
            raise DuplicateMealGoalsNameError
        # Add it;
        self._meal_goals['meal_name'] = meal_goals
