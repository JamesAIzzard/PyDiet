from typing import List, Dict

from model import flags

_flags = [
    flags.Flag(
        name="alcohol_free",
        nutrient_relations={
            "alcohol": flags.FlagImpliesNutrient.ZERO
        },
        direct_alias=True
    ),
    flags.Flag(name="caffiene_free"),
    flags.Flag(name="dairy_free"),
    flags.Flag(name="gluten_free"),
    flags.Flag(name="nut_free"),
    flags.Flag(name="vegan"),
    flags.Flag(name="vegetarian")
]
all_flags = {f.name: f for f in _flags}
