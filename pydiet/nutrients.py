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

def print_nutrient_targets_menu(subject:'INutrientTargetable')->str:
    output = ''
    if len(subject.nutrient_targets):
        for i,nutrient_name in enumerate(subject.nutrient_targets.keys(), start=1):
            output = output + '{num}. {nutrient_name} - {nutrient_qty}{nutrient_qty_units}'.format(
                num=i,
                nutrient_name=nutrient_name,
                nutrient_qty=subject.nutrient_targets[nutrient_name][0],
                nutrient_qty_units=subject.nutrient_targets[nutrient_name][1])
    else:
        output = 'No nutrient targets assigned.'
    return output