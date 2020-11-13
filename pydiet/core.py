from typing import List, Dict

from pydiet import configs, FlagNutrientRelation

flag_nutrient_relations: Dict[str, List['FlagNutrientRelation']] = {}
nutrient_flag_relations: Dict[str, List['FlagNutrientRelation']] = {}

# Populate the flag-nutrient mappings;
for flag_name, relations in configs.flag_nutrient_relations.items():
    flag_nutrient_relations[flag_name] = []
    for nutrient_name, implies_has_nutrient in relations:
        relation = FlagNutrientRelation(flag_name, nutrient_name, implies_has_nutrient)
        flag_nutrient_relations[flag_name].append(relation)
        if nutrient_name not in nutrient_flag_relations:
            nutrient_flag_relations[nutrient_name] = []
        nutrient_flag_relations[nutrient_name].append(relation)
