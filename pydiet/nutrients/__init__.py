from typing import Dict

from .has_nutrient_ratios import HasNutrientRatios, HasSettableNutrientRatios, NutrientRatioData
from .nutrient import Nutrient
from .core import get_nutrient_primary_name, all_primary_and_alias_nutrient_names
from . import configs, exceptions, validation

# Init the global nutrient instances;
global_nutrients: Dict[str, 'Nutrient'] = {}

for nutrient_name in configs.all_primary_nutrient_names:
    if nutrient_name not in global_nutrients.keys():
        global_nutrients[nutrient_name] = nutrient.Nutrient(nutrient_name)
