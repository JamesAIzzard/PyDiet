from typing import List, Dict
from difflib import SequenceMatcher
from heapq import nlargest

from model import nutrients
from . import validation, configs, exceptions

# Init the global nutrient instances;
global_nutrients: Dict[str, 'nutrients.Nutrient'] = {}


def init_global_nutrients() -> None:
    """Constructs the global list of nutrients for use across the model."""
    for primary_nutrient_name in configs.all_primary_nutrient_names:
        if primary_nutrient_name not in global_nutrients.keys():
            global_nutrients[primary_nutrient_name] = nutrients.Nutrient(primary_nutrient_name)


def get_all_primary_and_alias_nutrient_names() -> List[str]:
    """Returns a list of all nutrient names, primary and alias."""
    names = []
    for nutrient_name in configs.all_primary_nutrient_names:
        names.append(nutrient_name)
    for nutrient_aliases in configs.nutrient_aliases.values():
        for alias in nutrient_aliases:
            names.append(alias)
    return names


def get_nutrient_primary_name(nutrient_name: str) -> str:
    """Converts any nutrient name into its primary name.
    Raises:
        NutrientNameError: To indicate the nutrient name was not valid.
    """
    # Validate the name first;
    nutrient_name = validation.validate_nutrient_name(nutrient_name)
    # Return if primary already;
    if nutrient_name in configs.all_primary_nutrient_names:
        return nutrient_name
    # Now search through the aliases;
    nas = configs.nutrient_aliases
    for primary_name in nas.keys():
        if nutrient_name in nas[primary_name]:
            return primary_name
    # Nothing found - error;
    raise exceptions.NutrientNameError


def get_n_closest_nutrient_names(search_term: str, num_results: int = 5) -> List[str]:
    """Returns a list of n nutrient names matching the search term most closely."""
    scores = {}
    for nutrient_name in nutrients.get_all_primary_and_alias_nutrient_names():
        scores[nutrient_name] = SequenceMatcher(None, search_term, nutrient_name).ratio()
    return nlargest(num_results, scores, key=scores.get)

# def score_similarity(words_to_score: List[str], search_term: str) -> Dict[str, float]:
#     scores = {}
#     for word in words_to_score:
#         scores[word] = SequenceMatcher(None, search_term, word).ratio()
#     return scores
#
# all_names = get_saved_unique_values(subject_type)
# all_scores = score_similarity(all_names, search_term)
# return nlargest(num_results, all_scores, key=all_scores.get)
