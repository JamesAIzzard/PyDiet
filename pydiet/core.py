from typing import List, Dict, TYPE_CHECKING

import pydiet
from pydiet import configs

if TYPE_CHECKING:
    from pydiet import FlagNutrientRelation

flag_nutrient_relations: Dict[str, List['FlagNutrientRelation']] = {}  # Flag names for keys;
nutrient_flag_relations: Dict[str, List['FlagNutrientRelation']] = {}  # Nutrient names for keys;


def build_flag_nutrient_rel_maps() -> None:
    # Populate the flag-nutrient mappings;
    for flag_name, relations in configs.flag_nutrient_relations.items():
        flag_nutrient_relations[flag_name] = []
        for nutrient_name, implies_has_nutrient in relations.items():
            relation = pydiet.FlagNutrientRelation(flag_name, nutrient_name, implies_has_nutrient)
            flag_nutrient_relations[flag_name].append(relation)
            if nutrient_name not in nutrient_flag_relations:
                nutrient_flag_relations[nutrient_name] = []
            nutrient_flag_relations[nutrient_name].append(relation)
