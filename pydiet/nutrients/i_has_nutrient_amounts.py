import abc
from typing import Dict, Union

from pydiet import nutrients


class IHasNutrientAmounts(abc.ABC):

    @abc.abstractproperty
    def nutrient_amounts(self) -> Dict[str, 'nutrients.nutrient_amount.NutrientAmount']:
        raise NotImplementedError

    @abc.abstractmethod
    def get_readonly_nutrient_amount_data(self, nutrient_name: str) -> Dict[str, Union[float, str]]:
        raise NotImplementedError

    @property
    def primary_nutrient_amounts(self) -> Dict[str, 'nutrients.nutrient_amount.NutrientAmount']:
        primary_nutrient_amounts = {}
        for primary_nutrient_name in nutrients.configs.primary_nutrient_names:
            primary_nutrient_amounts[primary_nutrient_name] = self.get_nutrient_amount(
                primary_nutrient_name)
        return primary_nutrient_amounts

    @property
    def secondary_nutrient_amounts(self) -> Dict[str, 'nutrients.nutrient_amount.NutrientAmount']:
        secondary_nutrient_amounts = {}
        for nutrient_name in nutrients.configs.all_nutrient_names:
            if not nutrient_name in nutrients.configs.primary_nutrient_names:
                secondary_nutrient_amounts[nutrient_name] = self.get_nutrient_amount(
                    nutrient_name)
        return secondary_nutrient_amounts

    @property
    def defined_secondary_nutrient_amounts(self) -> Dict[str, 'nutrients.nutrient_amount.NutrientAmount']:
        defined_secondary_nutrient_amounts = {}
        secondary_nutrients = self.secondary_nutrient_amounts
        for secondary_nutrient_name in secondary_nutrients.keys():
            if secondary_nutrients[secondary_nutrient_name].defined:
                defined_secondary_nutrient_amounts[secondary_nutrient_name] = secondary_nutrients[secondary_nutrient_name]
        return defined_secondary_nutrient_amounts

    def get_nutrient_amount(self, nutrient_name: str) -> 'nutrients.nutrient_amount.NutrientAmount':
        return self.nutrient_amounts[nutrient_name]
