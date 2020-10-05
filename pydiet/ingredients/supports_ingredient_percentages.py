import abc
from typing import Dict, TypedDict

class IngredientPercentageData(TypedDict):
    quantity: Optional[float]
    quantity_units: Optional[str]
    perc_increase: Optional[float]
    perc_decrease: Optional[float]

class SupportsIngredientPercentages():

    @property
    @abc.abstractmethod
    def _ingredient_composition(self) -> Dict[str, 'IngredientPercentageData']:
        raise NotImplementedError
