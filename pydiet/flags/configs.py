from typing import Dict, List

all_flag_names: List[str] = [
    "alcohol_free",
    "caffiene_free",
    "dairy_free",
    "gluten_free",
    "nut_free",
    "vegan",
    "vegetarian"
]

flag_nutrient_relations: Dict[str, Dict[str, bool]] = {
    "alcohol_free": {"alcohol": False}
}
