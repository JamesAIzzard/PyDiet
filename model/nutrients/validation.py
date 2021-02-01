from typing import TYPE_CHECKING

from model import nutrients

if TYPE_CHECKING:
    pass


def validate_nutrient_name(name: str) -> str:
    """Checks the nutrient name is valid. Raises exception if not.
    Raises:
        NutrientNameError: To indicate the nutrient name was not valid.
    """
    name = name.replace(' ', '_')
    if name in nutrients.all_primary_and_alias_nutrient_names():
        return name
    raise nutrients.exceptions.NutrientNameError


def validate_configs() -> None:
    """Runs a battery of tests to check the nutrient config files are valid."""
    apnn = nutrients.configs.all_primary_nutrient_names

    # Check there are no duplications on all_primary_nutrient_names;
    if not len(apnn) == len(set(apnn)):
        raise nutrients.exceptions.NutrientConfigsError('Duplicates exist in the all_primary_nutrient_names list.')

    # Check that nutrient_aliases.keys() are in all_primary_nutrient_names;
    for name in nutrients.configs.nutrient_aliases.keys():
        if name not in apnn:
            raise nutrients.exceptions.NutrientConfigsError(
                '{} is in nutrient_aliases.keys() but is not a primary nutrient name'.format(name))
    # Check that no nutrient_aliases.values() are also in primary_nutrient_names;
    for alias_list in nutrients.configs.nutrient_aliases.values():
        for name in alias_list:
            if name in apnn:
                raise nutrients.exceptions.NutrientConfigsError(
                    '{} is listed as an alias but is also a primary nutrient name'.format(name))

            # Check that nutrient_group_definitions.keys() are in all_primary_nutrient_names;
    for name in nutrients.configs.nutrient_group_definitions.keys():
        if name not in apnn:
            raise nutrients.exceptions.NutrientConfigsError(
                '{} is a group definition key, but is not a primary nutrient name'.format(name))
    # Check that nutrient_group_definitions.values() are in all_primary_nutrient_names;
    for group_name in nutrients.configs.nutrient_group_definitions.keys():
        for name in nutrients.configs.nutrient_group_definitions[group_name]:
            if name not in apnn:
                raise nutrients.exceptions.NutrientConfigsError(
                    '{} is in included in the group {} but is not a primary nutrient name'.format(name, group_name))

    # Check that all calorie_nutrients.keys() are in all_primary_nutrient_names;
    for name in nutrients.configs.calorie_nutrients.keys():
        if name not in apnn:
            raise nutrients.exceptions.NutrientConfigsError(
                '{} is in calorie_nutrients.keys() but is not a primary nutrient name'.format(name))
