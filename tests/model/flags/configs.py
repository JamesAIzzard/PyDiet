import model

TEST_FLAG_CONFIGS = {
    "foo_free": {  # Direct alias depending on multiple nutrients.
        "nutrient_relations": {
            "foo": model.flags.FlagImpliesNutrient.zero,
            "foobing": model.flags.FlagImpliesNutrient.non_zero,
            "foobar": model.flags.FlagImpliesNutrient.zero,
        },
        "direct_alias": True
    },
    "pongaterian": {  # Indirect alias depending on multiple nutrients.
        "nutrient_relations": {
            "foo": model.flags.FlagImpliesNutrient.zero,
            "foobing": model.flags.FlagImpliesNutrient.zero,
            "bazing": model.flags.FlagImpliesNutrient.non_zero
        },
        "direct_alias": False
    },
    "foogetarian": {  # Direct alias depending on no nutrients.
        "nutrient_relations": {},
        "direct_alias": False
    },
    "bar_free": {  # Indirect alias depending on no nutrients.
        "nutrient_relations": {},
        "direct_alias": False
    }
}