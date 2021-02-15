from enum import Enum


class FlagImpliesNutrient(Enum):
    zero = 1
    non_zero = 2


flag_data = {
    "alcohol_free": {
        "nutrient_relations": {
            "alcohol": FlagImpliesNutrient.zero
        },
        "direct_alias": True
    },
    "caffiene_free": {"nutrient_relations": {}, "direct_alias": False},
    "dairy_free": {"nutrient_relations": {}, "direct_alias": False},
    "gluten_free": {"nutrient_relations": {}, "direct_alias": False},
    "nut_free": {"nutrient_relations": {}, "direct_alias": False},
    "vegan": {"nutrient_relations": {}, "direct_alias": False},
    "vegetarian": {"nutrient_relations": {}, "direct_alias": False}
}
