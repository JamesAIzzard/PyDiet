from .exceptions import (
    NutrientNameNotRecognisedError,
    NutrientConfigsError,
)
from . import main
from .configs import (
    ALL_PRIMARY_NUTRIENT_NAMES,
    NUTRIENT_ALIASES,
    NUTRIENT_GROUP_DEFINITIONS,
    CALORIE_NUTRIENTS
)


def validate_nutrient_name(nutrient_name: str) -> str:
    """Checks the nutrient name is valid. Raises exception if not.
    Raises:
        NutrientNameError: To indicate the nutrient name was not valid.
    """
    nutrient_name = nutrient_name.lower().replace(' ', '_')
    if nutrient_name in main.PRIMARY_AND_ALIAS_NUTRIENT_NAMES:
        return nutrient_name
    raise NutrientNameNotRecognisedError(nutrient_name=nutrient_name)


def validate_configs() -> None:
    """Runs a battery of tests to check the nutrient config files are valid."""
    apnn = ALL_PRIMARY_NUTRIENT_NAMES

    # Check there are no duplications on all_primary_nutrient_names;
    if not len(apnn) == len(set(apnn)):
        raise NutrientConfigsError(
            error_msg='Duplicates exist in the all_primary_nutrient_names list.'
        )

    # Check that nutrient_aliases.keys() are in all_primary_nutrient_names;
    for name in NUTRIENT_ALIASES.keys():
        if name not in apnn:
            raise NutrientConfigsError(
                error_msg=f'{name} is in nutrient_aliases.keys() but is not a primary nutrient name'
            )

    # Check that no nutrient_aliases.values() are also in primary_nutrient_names;
    for alias_list in NUTRIENT_ALIASES.values():
        for name in alias_list:
            if name in apnn:
                raise NutrientConfigsError(
                    error_msg=f'{name} is listed as an alias but is also a primary nutrient name.'
                )

    # Check that nutrient_group_definitions.keys() are in all_primary_nutrient_names;
    for name in NUTRIENT_GROUP_DEFINITIONS.keys():
        if name not in apnn:
            raise NutrientConfigsError(
                error_msg=f'{name} is a group definition key, but is not a primary nutrient name.'
            )

    # Check that nutrient_group_definitions.values() are in all_primary_nutrient_names;
    for group_name in NUTRIENT_GROUP_DEFINITIONS.keys():
        for name in NUTRIENT_GROUP_DEFINITIONS[group_name]:
            if name not in apnn:
                raise NutrientConfigsError(
                    error_msg=f'{name} is in included in the group {group_name} but is not a primary nutrient name.'
                )

    # Check that all calorie_nutrients.keys() are in all_primary_nutrient_names;
    for name in CALORIE_NUTRIENTS.keys():
        if name not in apnn:
            raise NutrientConfigsError(
                error_msg='{} is in calorie_nutrients.keys() but is not a primary nutrient name.'
            )
