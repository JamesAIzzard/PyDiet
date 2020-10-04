import abc
from typing import Dict

class SupportsIngredientRatios(abc.ABC):

    @property
    @abc.abstractmethod
    def _ingredient_ratios(self) -> Dict[str, 'CompositionTolerance']:
        ...


class SupportsSettableIngredientRatios(SupportsIngredientRatios, abc.ABC):

    def add_ingredient_perc(self, ingredient_name: str, nominal_perc: float, allowable_perc_inc: float,
                             allowable_perc_dec: float) -> None:
        ...

    def remove_ingredient_perc(self, ingredient_name: str) -> None:
        ...

    def edit_ingredient_perc(self, ingredient_name: str) -> None:
