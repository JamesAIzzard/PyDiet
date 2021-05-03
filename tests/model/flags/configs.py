import model

TEST_FLAG_CONFIGS = {
    "foo_free": {
        "nutrient_relations": {
            "foo": model.flags.FlagImpliesNutrient.zero,
            "foobing": model.flags.FlagImpliesNutrient.zero,
            "foobar": model.flags.FlagImpliesNutrient.zero,
        },
        "direct_alias": True
    },
    "pongaterian": {
        "nutrient_relations": {
            "foo": model.flags.FlagImpliesNutrient.zero,
            "foobing": model.flags.FlagImpliesNutrient.zero,
        },
        "direct_alias": False
    },
    "foogetarian": {
        "nutrient_relations": {},
        "direct_alias": False
    },
    "bar_free": {
        "nutrient_relations": {
            "bar": model.flags.FlagImpliesNutrient.zero
        },
        "direct_alias": False
    }
}