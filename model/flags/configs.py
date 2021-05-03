from .main import FlagImpliesNutrient

FLAG_CONFIGS = {
    "alcohol_free": {
        "nutrient_relations": {
            "alcohol": FlagImpliesNutrient.zero
        },
        "direct_alias": True
    },
    "caffeine_free": {
        "nutrient_relations": {
            "caffeine": FlagImpliesNutrient.zero
        },
        "direct_alias": True},
    "lactose_free": {
        "nutrient_relations": {
            "lactose": FlagImpliesNutrient.zero
        },
        "direct_alias": True},
    "gluten_free": {
        "nutrient_relations": {
            "gluten": FlagImpliesNutrient.zero
        },
        "direct_alias": True},
    "nut_free": {"nutrient_relations": {}, "direct_alias": False},
    "vegan": {"nutrient_relations": {}, "direct_alias": False},
    "vegetarian": {"nutrient_relations": {}, "direct_alias": False}
}
