from typing import Dict, Optional

from model import ingredients, nutrients, flags, quantity, persistence


def get_empty_ingredient_data() -> ingredients.IngredientData:
    """Returns a ingredient data dict with the starting default values set."""
    # Build the flags data;
    flags_data: Dict[str, Optional[bool]] = {f.name: None for f in flags.configs.all_flags.keys()}
    # Build the nutrients data that goes in the ingredient instance;
    nutrients_data: Dict[str, 'nutrients.NutrientRatioData'] = {}
    for nutrient_name in nutrients.all_primary_nutrient_names:
        nutrients_data[nutrient_name] = nutrients.get_empty_nutrient_ratio_data()
    return ingredients.IngredientData(
        cost_per_g=None,
        flags=flags_data,
        name=None,
        nutrients=nutrients_data,
        bulk=quantity.BulkData(
            pref_unit='g',
            ref_qty=100,
            g_per_ml=None,
            piece_mass_g=None
        )
    )


def load_new_ingredient() -> ingredients.Ingredient:
    """Creates and returns a fresh ingredient instance with no data filled in."""
    return ingredients.Ingredient(get_empty_ingredient_data())


def get_ingredient_name(datafile_name: str) -> str:
    """Returns the ingredient name corresponding to the datafile name."""
    return persistence.get_unique_value_from_datafile_name(cls=ingredients.Ingredient, datafile_name=datafile_name)
