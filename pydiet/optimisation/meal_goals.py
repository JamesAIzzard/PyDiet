from typing import TYPE_CHECKING, Dict, Optional, List, Tuple

from pydiet import time, nutrients, flags, tags

if TYPE_CHECKING:
    from pydiet.optimisation.day_goals import DayGoals

data_template = {
    "time": None,
    "max_cost_gbp": None,
    "flags": [],
    "tags": [],
    "calories": None,
    "perc_fat": None,
    "perc_carbs": None,
    "perc_protein": None,
    "nutrient_mass_targets": {}
}


class MealGoals(
    flags.IFlaggable, 
    nutrients.INutrientTargetable,
    tags.ITaggable):
    def __init__(self, name, parent_day_goals: 'DayGoals'):
        self._name = name
        self._parent_day_goals = parent_day_goals

    @property
    def data(self) -> Dict:
        return self._parent_day_goals._data['meal_goals'][self.name]

    @property
    def parent_day_goals(self) -> 'DayGoals':
        return self._parent_day_goals

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        # Stash the old name;
        old_name = self._name
        # Set the name locally;
        self._name = value
        # Update the name in the dict on the parent;
        self._parent_day_goals.meal_goals[value] = self._parent_day_goals.meal_goals[old_name]

    @property
    def time(self) -> str:
        return self.data['time']

    @time.setter
    def time(self, value: str) -> None:
        # Write to the data;
        self.data['time'] = time.parse_time(value)

    @property
    def max_cost_gbp(self) -> float:
        return self.data['max_cost_gbp']

    @max_cost_gbp.setter
    def max_cost_gbp(self, value: float) -> None:
        self.data['max_cost_gbp'] = value

    @property
    def flags(self) -> List[str]:
        return self.data['flags']

    def add_flag(self, flag_name: str) -> None:
        raise NotImplementedError

    def remove_flag(self, flag_name: str) -> None:
        raise NotImplementedError

    @property
    def tags(self) -> List[str]:
        return self.data['tags']

    def add_tag(self, tag: str) -> None:
        raise NotImplementedError

    def remove_tag(self, tag: str) -> None:
        raise NotImplementedError

    @property
    def perc_protein(self) -> float:
        return round(float(self.data['perc_protein']), 0)

    @perc_protein.setter
    def perc_protein(self, value: float) -> None:
        self.data['perc_protein']

    @property
    def perc_carbs(self) -> float:
        return round(float(self.data['perc_carbs']), 0)

    @perc_carbs.setter
    def perc_carbs(self, value: float) -> None:
        self.data['perc_carbs']

    @property
    def perc_fat(self) -> float:
        return round(float(self.data['perc_fat']), 0)

    @perc_fat.setter
    def perc_fat(self, value: float) -> None:
        self.data['perc_fat']

    @property
    def calories(self) -> float:
        return self.data['calories']

    @calories.setter
    def calories(self, value: float) -> None:
        self.data['calories'] = value

    @property
    def perc_of_day_cals(self) -> Optional[float]:
        if not self.calories == None and \
                not self.parent_day_goals.calories == None:
            return round(
                (self.calories/self.parent_day_goals.calories)*100, 1)
        else:
            return None

    @property
    def nutrient_targets(self) -> Dict[str, Tuple[float, str]]:
        return self.data['nutrient_targets']
    
    def add_nutrient_target(self, nutrient_name: str, nutrient_qty: float, nutrient_qty_units: str) -> None:
        raise NotImplementedError

    def remove_nutrient_target(self, nutrient_name: str) -> None:
        raise NotImplementedError