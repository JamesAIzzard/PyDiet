"""General functions for the nutrient module."""
from difflib import SequenceMatcher
from heapq import nlargest
from typing import List

import model


def get_nutrient_primary_name(nutrient_name: str) -> str:
    """Converts any nutrient name into its primary name.
    Raises:
        NutrientNameError: To indicate the nutrient name was not valid.
    """

    # Validate the name first;
    nutrient_name = model.nutrients.validation.validate_nutrient_name(nutrient_name)

    # Return if primary already;
    if nutrient_name in model.nutrients.configs.ALL_PRIMARY_NUTRIENT_NAMES:
        return nutrient_name

    # Not primary, so search through the aliases;
    nas = model.nutrients.configs.NUTRIENT_ALIASES
    for primary_name in nas.keys():
        if nutrient_name in nas[primary_name]:
            return primary_name

    # Nothing found - error;
    raise model.nutrients.exceptions.NutrientNameNotRecognisedError(nutrient_name=nutrient_name)


def get_nutrient_alias_names(nutrient_name: str) -> List[str]:
    """Returns a list of known aliases for the primary nutrient name provided."""
    # Make sure we have the primary name for this nutrient;
    nutrient_name = get_nutrient_primary_name(nutrient_name)
    # Grab the nutrient and return its alias names;
    return model.nutrients.GLOBAL_NUTRIENTS[nutrient_name].alias_names


def get_calories_per_g(nutrient_name: str) -> float:
    """Returns the number of calories in a gram of the nutrient."""
    # Make sure we have the primary name;
    nutrient_name = get_nutrient_primary_name(nutrient_name)
    # Grab the nutrient and return its cals_per_g;
    return model.nutrients.GLOBAL_NUTRIENTS[nutrient_name].calories_per_g


def get_n_closest_nutrient_names(search_term: str, num_results: int = 5) -> List[str]:
    """Returns a list of n nutrient names matching the search term most closely."""
    scores = {}
    for nutrient_name in model.nutrients.PRIMARY_AND_ALIAS_NUTRIENT_NAMES:
        scores[nutrient_name] = SequenceMatcher(None, search_term, nutrient_name).ratio()
    return nlargest(num_results, scores, key=scores.get)
