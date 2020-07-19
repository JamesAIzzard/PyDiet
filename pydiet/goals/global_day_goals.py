from typing import Optional, List

from singleton_decorator import singleton

import pydiet
from pydiet import flags, repository, ingredients, goals

_DATA_TEMPLATE = {
  "calories": None,
  "flags": [],
  "max_cost_gbp": None,
  "nutrient_mass_targets": {}
}

@singleton
class GlobalDayGoals(flags.i_has_flags.IHasFlags):
    def __init__(self):
        self._data = repository.repository_service.read_global_day_goals_data()

    @property
    def max_cost_gbp(self) -> Optional[float]:
        return self._data['max_cost_gbp']

    @max_cost_gbp.setter
    def max_cost_gbp(self, value:float)->None:
        value = float(value)
        if value < 0: 
            raise ValueError
        self._data['max_cost_gbp'] = value

    @property
    def calories(self) -> Optional[float]:
        return self._data['calories']

    @calories.setter
    def calories(self, value:float)->None:
        value = float(value)
        if value < 0: 
            raise ValueError
        self._data['calories'] = value        

    def _perc_setter(self, name:str, value:float) -> None:
        value = float(value)
        if value < 0 or value > 100: 
            raise ValueError
        self._data['perc_{}'.format(name)] = value

    @property
    def perc_fat(self) -> Optional[float]:
        return self._data['perc_fat']

    @perc_fat.setter
    def perc_fat(self, value:float) ->None:
        self._perc_setter('fat', value)

    @property
    def perc_carbs(self) -> float:
        return self._data['perc_carbs']

    @perc_carbs.setter
    def perc_carbs (self, value:float) -> None:
        self._perc_setter('carbs', value)

    @property
    def perc_protein(self) -> float:
        return self._data['perc_protein']

    @perc_protein.setter
    def perc_protein(self, value:float) -> None:
        self._perc_setter('protein', value)

    @property
    def flags(self) -> List[str]:
        return self._data['flags']

    def add_flag(self, flag_name:str)->None:
        # Check the flag name is a valid flag;
        if not flag_name in flags.configs.FLAGS:
            raise ValueError
        if not flag_name in self._data['flags']:
            self._data['flags'].append(flag_name)

    def remove_flag(self, flag_name:str)->None:
        if flag_name in self._data['flags']:
            self._data['flags'].remove(flag_name)

    def validate(self)->None:
        # Check the percentage sums do not exceed 100%;
        perc_sum = self.perc_fat+self.perc_protein+self.perc_carbs
        if not perc_sum == 100:
            raise pydiet.exceptions.PercentageSumError

    def save(self) -> None:
        # Run validation checks;
        self.validate()
        # Save the file;
        repository.repository_service.update_global_day_goals_data(self._data)