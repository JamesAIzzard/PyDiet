import abc
from typing import Dict, Tuple

class INutrientTargetable(abc.ABC):

    @abc.abstractproperty
    def nutrient_targets(self)-> Dict[str, Tuple[float, str]]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_nutrient_target(self, nutrient_name:str, nutrient_qty:float, nutrient_qty_units: str)->None:
        raise NotImplementedError

    @abc.abstractmethod
    def remove_nutrient_target(self, nutrient_name:str)->None:
        raise NotImplementedError

