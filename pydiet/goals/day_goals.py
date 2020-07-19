from typing import Dict, Optional, List, Tuple, TYPE_CHECKING

from pydiet import flags, nutrients, goals


if TYPE_CHECKING:
    from pydiet.goals.meal_goals import MealGoals

DATA_TEMPLATE = {
    "name": None,
    "solution_datafile_names": {},
    "max_cost_gbp": None,
    "flags": [],
    "calories": None,
    "nutrient_mass_targets": {},
    "meal_goals": {}
}


class DayGoals(flags.i_has_flags.IHasFlags,
               nutrients.i_has_nutrient_targets.IHasNutrientTargets):
    def __init__(self, data: Dict):
        self._data = data
        # Populate the list of meal goal objects;
        self._meal_goals: Dict[str, 'MealGoals'] = {}
        for mg_name in self._data['meal_goals'].keys():
            self._meal_goals[mg_name] = goals.meal_goals.MealGoals(
                mg_name, self)

    @property
    def name(self) -> str:
        return self._data['name']

    @name.setter
    def name(self, value: str) -> None:
        self._data['name'] = value

    @property
    def max_cost_gbp(self) -> Optional[float]:
        return self._data['max_cost_gbp']

    @max_cost_gbp.setter
    def max_cost_gbp(self, value: float) -> None:
        self._data['max_cost_gbp'] = value

    @property
    def flags(self) -> List[str]:
        return self._data['flags']

    def add_flag(self, flag_name: str) -> None:
        # Check the flag name is valid;
        if not flag_name in flags.FLAGS:
            raise flags.FlagNameError
        # Add the flag if it isn't already there;
        if not flag_name in self.flags:
            self._data['flags'].append(flag_name)

    def remove_flag(self, flag_name: str) -> None:
        # Check the flag name is valid;
        if not flag_name in flags.FLAGS:
            raise flags.FlagNameError
        # Remove the flag if it is in the list;
        if flag_name in self.flags:
            self._data['flags'].remove(flag_name)

    @property
    def calories(self) -> Optional[float]:
        return self._data['calories']

    @property
    def nutrient_targets(self) -> Dict[str, Tuple[float, str]]:
        return self._data['nutrient_targets']

    def add_nutrient_target(self, nutrient_name: str, nutrient_qty: float, nutrient_qty_units: str) -> None:
        # Check the nutrient name is legit;
        # Check the nutrient target doesn't exceed the macro's;
        # Check the nutrient target doesn't exceed another nutrient target;
        # Check the nutrient target doesn't exceed a global target;
        # Write the nutrient target;
        self._data['nutrient_targets'][nutrient_name] = (
            nutrient_qty, nutrient_qty_units)

    def remove_nutrient_target(self, nutrient_name: str) -> None:
        # Remove the element;
        del self._data['nutrient_targets'][nutrient_name]

    @property
    def meal_goals(self) -> Dict[str, 'MealGoals']:
        return self._meal_goals

    def add_new_meal_goal(self, meal_name: str) -> 'MealGoals':
        # Check there isn't a meal by this name already;
        if meal_name in self.meal_goals.keys():
            raise DuplicateMealGoalsNameError

        # Create new meal goals instance and add it to the data
        # and the dict;
        self._data['meal_goals'][meal_name] = meal_goals.data_template
        mg = meal_goals.MealGoals(meal_name, self)
        self.meal_goals[meal_name] = mg

        # Also return the mealgoals instance;
        return mg

    def remove_meal_goal(self, meal_name: str) -> None:
        raise NotImplementedError
