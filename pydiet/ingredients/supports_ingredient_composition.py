import abc
from typing import Dict, TypedDict


class IngredientCompositionData(TypedDict):
    quantity: Optional[float]
    quantity_units: Optional[str]
    perc_increase: Optional[float]
    perc_decrease: Optional[float]


class SupportsIngredientComposition():

    @property
    @abc.abstractmethod
    def _ingredient_composition_data(self) -> Dict[str, 'IngredientCompositionData']:
        raise NotImplementedError
