from typing import Dict

# Flag nutrient relations are defined as follows:
# - Flag name goes in outer dict.
# - Against each flag name, you can store a dict of nutrient names, and a boolean value to indicate
#   what the flag implies asbout the nutrient's presence. True indicates that the flag implies it *is*
#   present, while False indicates the flag implies the nutrient *is not* present.

class FlagNutrientRelations:


flag_nutrient_relations: Dict[str, Dict[str, bool]] = {
    "alcohol_free": {"alcohol": False}
}

class NutrientFlagRelation:
    def __init__(self, nutrient_name:str, flag_implies_has_nutrient:bool):
        self.nutrient_name = nutrient_name
        self.flag_implies_has_nutrient = flag_implies_has_nutrient