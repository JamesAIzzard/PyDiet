from typing import List, Dict, TYPE_CHECKING

from pydiet import nutrients
from pydiet.nutrients import validation, configs, exceptions

if TYPE_CHECKING:
    from pydiet.nutrients import Nutrient

# Init the global nutrient instances;
global_nutrients: Dict[str, 'Nutrient'] = {}


def build_global_nutrients() -> None:
    for primary_nutrient_name in configs.all_primary_nutrient_names:
        if primary_nutrient_name not in global_nutrients.keys():
            global_nutrients[primary_nutrient_name] = nutrients.Nutrient(primary_nutrient_name)


def all_primary_and_alias_nutrient_names() -> List[str]:
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
