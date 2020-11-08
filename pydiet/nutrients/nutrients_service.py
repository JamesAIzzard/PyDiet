from typing import List, Dict, TYPE_CHECKING

from pydiet import nutrients

if TYPE_CHECKING:
    from pydiet.nutrients.has_nutrient_ratios import NutrientData


def all_primary_and_alias_nutrient_names() -> List[str]:
    names = []
    for nutrient_name in nutrients.configs.all_primary_nutrient_names:
        names.append(nutrient_name)
    for nutrient_aliases in nutrients.configs.nutrient_aliases.values():
        for alias in nutrient_aliases:
            names.append(alias)
    return names


def validate_nutrient_name(name: str) -> str:
    name = name.replace(' ', '_')
    # Just return if all OK;
    if name in all_primary_and_alias_nutrient_names():
        return name
    # Wasn't found, so raise an exception;
    raise nutrients.exceptions.NutrientNameError


def get_nutrient_primary_name(nutrient_name: str) -> str:
    # Validate the name first;
    nutrient_name = validate_nutrient_name(nutrient_name)
    # Return if primary already;
    if nutrient_name in nutrients.configs.all_primary_nutrient_names:
        return nutrient_name
    # Now search through the aliases;
    nas = nutrients.configs.nutrient_aliases
    for primary_name in nas.keys():
        if nutrient_name in nas[primary_name]:
            return primary_name
    # Nothing found - error;
    raise nutrients.exceptions.NutrientNameError


def validate_nutritients_data(data: Dict[str, 'NutrientData']) -> None:
    ...
