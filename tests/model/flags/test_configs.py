"""Flag configuration for use during flag testing.
Having a dedicated flag configuration divorces the tests from any changes that might
happen on the real database.
"""
import model

FLAG_CONFIGS = {
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
    "tirbur_free": {
        "nutrient_relations": {
            "tirbur": model.flags.FlagImpliesNutrient.zero
        },
        "direct_alias": True
    },
    "foogetarian": {
        "nutrient_relations": {},
        "direct_alias": False
    },
    "bar_free": {  # Indirect alias depending on no nutrients.
        "nutrient_relations": {
            "bar": model.flags.FlagImpliesNutrient.zero
        },
        "direct_alias": False
    },
}
