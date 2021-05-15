from difflib import SequenceMatcher
from heapq import nlargest
from typing import List, Dict, Callable

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


def validate_nutrient_family_masses(nutrient_name: str, get_nutrient_mass_g: Callable[[str], float]) -> None:
    """Checks that the nutrient masses stated for the named nutrient's entire family do not conflict.
    Args:
        nutrient_name (str): The name of the nutrient to validate.
        get_nutrient_mass_g (float): Returns the mass in g or raises an UndefinedNutrientMassError.
    Notes:
        It would have been possible to implement this function as an abstract base class, something
        like `StoresNutrientMasses`. However, we want to use it on the  NutrientRatios base classes too,
        since they actually store their data as nutrient masses (per subject mass). It seemed like it would
        have been a little misleading to have `HasNutrientRatios` inherit from `StoresNutrientMasses` since
        there is a conceptual difference between nutrient ratios and nutrient masses.
        The other main issue with this approach, is that not all classes that have nutrient masses actually store
        them locally. For example, a RecipeAmount has nutrient masses, but derives them from the IngredientAmount
        instances it stores locally. So, if this validation check was written as a method on an object, it wouldn't
        always be operating on local data.
        Considering these factors, it seemed better to write this code as a function, instead of a method.
    """
    # Make sure we are dealing with the primary name;
    nutrient_name = model.nutrients.get_nutrient_primary_name(nutrient_name)

    # OK, grab a reference to the nutrient instance;
    nutrient = model.nutrients.GLOBAL_NUTRIENTS[nutrient_name]

    # Create a dict to store all defined and min values in the tree;
    check_values: Dict[str, Dict[str, float]] = {}
    for related_nutrient in list(nutrient.all_relative_nutrients.values()) + [nutrient]:
        try:
            stated_value = get_nutrient_mass_g(related_nutrient.primary_name)
        except model.nutrients.exceptions.UndefinedNutrientMassError:
            stated_value = None
        check_values[related_nutrient.primary_name] = {
            "stated_value": stated_value,
            "min_value": 0
        }

    # First grab a list of all nutrients in the tree which have no direct children. These
    # are the endpoints;
    endpoints: List['model.nutrients.Nutrient'] = []
    for related_nutrient in nutrient.all_relative_nutrients.values():
        if len(related_nutrient.direct_child_nutrients) == 0:
            endpoints.append(related_nutrient)

    # Define a function to check a single level of the tree;
    def check_level(level_member: 'model.nutrients.Nutrient') -> None:
        # OK, we need to check the level belonging to every parent of this level member, in case
        # it has multiple parents (i.e it is in multiple groups);
        for level_parent in level_member.direct_parent_nutrients.values():
            # Total up the defined nutrient mass in this level;
            min_value = 0
            for level_member in level_parent.direct_child_nutrients.values():
                try:
                    min_value += get_nutrient_mass_g(level_member.primary_name)
                except model.nutrients.exceptions.UndefinedNutrientMassError:
                    # OK, the nutrient mass isn't defined, can we use a min value we have already calculated?
                    if check_values[level_member.primary_name] is not None:
                        # Yep, we have a min value defined, use that;
                        min_value += check_values[level_member.primary_name]["min_value"]

            # Is this min value greater than a min value assigned to this level parent already?
            if check_values[level_parent.primary_name]['min_value'] < min_value:
                check_values[level_parent.primary_name]['min_value'] = min_value

            # If the parent has a stated value, then check the min value doesn't exceed it;
            if check_values[level_parent.primary_name]["stated_value"] is not None:
                if check_values[level_parent.primary_name]["min_value"] > \
                        check_values[level_parent.primary_name]["stated_value"]:
                    raise model.nutrients.exceptions.ChildNutrientExceedsParentMassError(
                        nutrient_group_name=level_parent.primary_name
                    )

            # Now go ahead and do the same check on the next level up;
            check_level(level_parent)

    # Start the process by level checking for each endpoint;
    for endpoint in endpoints:
        check_level(endpoint)


def get_n_closest_nutrient_names(search_term: str, num_results: int = 5) -> List[str]:
    """Returns a list of n nutrient names matching the search term most closely."""
    scores = {}
    for nutrient_name in model.nutrients.PRIMARY_AND_ALIAS_NUTRIENT_NAMES:
        scores[nutrient_name] = SequenceMatcher(None, search_term, nutrient_name).ratio()
    return nlargest(num_results, scores, key=scores.get)
