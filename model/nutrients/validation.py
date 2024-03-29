"""Valdiation functions for the nutrient module."""
from typing import Dict, List, Callable

import model


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
        """Function to check a single level of the tree."""
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


def validate_nutrient_name(nutrient_name: str) -> str:
    """Checks the nutrient name is valid. Raises exception if not.
    Raises:
        NutrientNameError: To indicate the nutrient name was not valid.
    """
    nutrient_name = nutrient_name.lower().replace(' ', '_')
    if nutrient_name in model.nutrients.PRIMARY_AND_ALIAS_NUTRIENT_NAMES:
        return nutrient_name
    raise model.nutrients.exceptions.NutrientNameNotRecognisedError(nutrient_name=nutrient_name)


def validate_configs(configs: 'model.nutrients.configs') -> None:
    """Runs a battery of tests to check the nutrient config files are valid."""
    apnn = configs.ALL_PRIMARY_NUTRIENT_NAMES

    # Check there are no duplications on all_primary_nutrient_names;
    if not len(apnn) == len(set(apnn)):
        raise model.nutrients.exceptions.NutrientConfigsError(
            error_msg='Duplicates exist in the all_primary_nutrient_names list.'
        )

    # Check that nutrient_aliases.keys() are in all_primary_nutrient_names;
    for name in configs.NUTRIENT_ALIASES.keys():
        if name not in apnn:
            raise model.nutrients.exceptions.NutrientConfigsError(
                error_msg=f'{name} is in nutrient_aliases.keys() but is not a primary nutrient name'
            )

    # Check that no nutrient_aliases.values() are also in primary_nutrient_names;
    for alias_list in configs.NUTRIENT_ALIASES.values():
        for name in alias_list:
            if name in apnn:
                raise model.nutrients.exceptions.NutrientConfigsError(
                    error_msg=f'{name} is listed as an alias but is also a primary nutrient name.'
                )

    # Check that nutrient_group_definitions.keys() are in all_primary_nutrient_names;
    for name in configs.NUTRIENT_GROUP_DEFINITIONS.keys():
        if name not in apnn:
            raise model.nutrients.exceptions.NutrientConfigsError(
                error_msg=f'{name} is a group definition key, but is not a primary nutrient name.'
            )

    # Check that nutrient_group_definitions.values() are in all_primary_nutrient_names;
    for group_name in configs.NUTRIENT_GROUP_DEFINITIONS.keys():
        for name in configs.NUTRIENT_GROUP_DEFINITIONS[group_name]:
            if name not in apnn:
                raise model.nutrients.exceptions.NutrientConfigsError(
                    error_msg=f'{name} is in included in the group {group_name} but is not a primary nutrient name.'
                )

    # Check that all mandatory nutrient names are also primary names;
    for mandatory_nutr_name in configs.MANDATORY_NUTRIENT_NAMES:
        if mandatory_nutr_name not in configs.ALL_PRIMARY_NUTRIENT_NAMES:
            raise model.nutrients.exceptions.NutrientConfigsError(
                error_msg=f'{mandatory_nutr_name} is listed as mandatory but is not a primary name.'
            )

    # Check that all calorie_nutrients.keys() are in all_primary_nutrient_names;
    for name in configs.CALORIE_NUTRIENTS.keys():
        if name not in apnn:
            raise model.nutrients.exceptions.NutrientConfigsError(
                error_msg='{} is in calorie_nutrients.keys() but is not a primary nutrient name.'
            )
