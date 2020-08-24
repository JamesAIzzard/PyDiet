import abc
from typing import Dict

from pydiet import nutrients


class IHasNutrientAmounts(abc.ABC):

    @property
    def primary_nutrients(self) -> Dict[str, 'nutrients.nutrient_amount.NutrientAmount']:
        primary_nutrients = {}
        for primary_nutrient_name in nutrients.configs.primary_nutrient_names:
            primary_nutrients[primary_nutrient_name] = self.get_nutrient_amount(primary_nutrient_name)
        return primary_nutrients

    @property
    def secondary_nutrients(self) -> Dict[str, 'nutrients.nutrient_amount.NutrientAmount']:
        secondary_nutrients = {}
        for nutrient_name in nutrients.configs.all_nutrient_names:
            if not nutrient_name in nutrients.configs.primary_nutrient_names:
                secondary_nutrients[nutrient_name] = self.get_nutrient_amount(
                    nutrient_name)
        return secondary_nutrients

    @property
    def defined_secondary_nutrients(self) -> Dict[str, 'nutrients.nutrient_amount.NutrientAmount']:
        defined_secondary_nutrients = {}
        secondary_nutrients = self.secondary_nutrients
        for secondary_nutrient_name in secondary_nutrients.keys():
            if secondary_nutrients[secondary_nutrient_name].defined:
                defined_secondary_nutrients[secondary_nutrient_name] = secondary_nutrients[secondary_nutrient_name]
        return defined_secondary_nutrients

    @abc.abstractmethod
    def get_nutrient_amount(self, nutrient_name: str) -> 'nutrients.nutrient_amount.NutrientAmount':
        raise NotImplementedError

    def set_nutrient_amount(self,
                            nutrient_name: str,
                            ingredient_qty: float,
                            ingredient_qty_units: str,
                            nutrient_mass: float,
                            nutrient_mass_units: str) -> None:
        na = self.get_nutrient_amount(nutrient_name)
        na.ingredient_qty = ingredient_qty
        na.ingredient_qty_units = ingredient_qty_units
        na.nutrient_mass = nutrient_mass
        na.nutrient_mass_units = nutrient_mass_units
