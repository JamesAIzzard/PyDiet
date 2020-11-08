from typing import Dict, TYPE_CHECKING

from .has_nutrient_ratios import HasNutrientRatios, HasSettableNutrientRatios

# Init the global nutrient instances;
global_nutrients: Dict[str, nutrient.Nutrient] = {}

for nutrient_name in configs.all_primary_nutrient_names:
    if nutrient_name not in global_nutrients.keys():
        global_nutrients[nutrient_name] = nutrient.Nutrient(nutrient_name)
