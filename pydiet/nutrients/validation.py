from typing import TYPE_CHECKING

from pydiet import nutrients
from pydiet.nutrients import exceptions

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
    raise exceptions.NutrientNameError
