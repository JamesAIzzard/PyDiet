from typing import Optional

from singleton_decorator import singleton

from pydiet import repository_service as rps

@singleton
class GlobalDayGoals():
    def __init__(self):
        self._data = rps.read_global_day_goals_data()

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

            