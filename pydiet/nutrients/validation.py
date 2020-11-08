from typing import Dict, TYPE_CHECKING

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


def validate_nutrient_data(nutrient_data: 'NutrientRatioData') -> 'NutrientRatioData':
    # Check the nutrient qty does not exceed the parent ingredient qty;
    if nutrient_data['nutrient_g_per_subject_g'] is not None and nutrient_data['nutrient_g_per_subject_g'] > 1:
        raise nutrients.exceptions.NutrientQtyExceedsIngredientQtyError
    # Check the pref units are valid and of type mass;
    nutrient_data['nutrient_pref_units'] = quantity.core.validate_qty_unit(
        nutrient_data['nutrient_pref_units'])
    if nutrient_data['nutrient_pref_units'] not in quantity.core.get_recognised_mass_units():
        raise quantity.exceptions.IncorrectUnitTypeError
    return nutrient_data


def validate_nutrients_data(nutrients_data: Dict[str, 'NutrientData']) -> Dict[str, 'NutrientData']:
    for nutrient_name in nutrients_data:

        # Verify the name is on the list of primary names;
        if nutrient_name not in nutrients.configs.all_primary_nutrient_names:
            raise nutrients.exceptions.NutrientNameError('{} is not a primary nutrient name.'.format(nutrient_name))

        # Validate the nutrient data in isolation;
        nutrients_data[nutrient_name] = validate_nutrient_data(nutrients_data[nutrient_name])

    for nutrient_name in nutrients_data:
        # Check the child nutrient does not exceed it's parent's quantity;
        # .Grab a list of parent nutrients;
        parent_nutrients = nutrients.global_nutrients[nutrient_name].parent_nutrients
        # .For each one, check that the sum of their child nutrient qty's do not exceed their qty;
        for parent_nutrient_name in parent_nutrients:
            # ..Grab the qty of the parent nutrient;
            parent_g = nutrients_data[parent_nutrient_name]['nutrient_g_per_subject_g']
            # ..Skip to the next parent nutrient if this one isn't defined yet;
            if parent_g is None:
                continue
            # ..Sum up the g_masses of its children;
            child_g_sum: float = 0
            child_nutrients = parent_nutrients[parent_nutrient_name].child_nutrients
            for child_nutrient_name in child_nutrients:
                child_nutrient_g = nutrients_data[child_nutrient_name]['nutrient_g_per_subject_g']
                if child_nutrient_g is not None:
                    child_g_sum = child_g_sum + child_nutrient_g
            # ..Raise an exception of the child mass sum exceeds the parent's mass;
            if child_g_sum > parent_g * 1.01:  # *101% to prevent rounding error issues.
                raise nutrients.exceptions.ChildNutrientQtyExceedsParentNutrientQtyError(
                    'The qty of child nutrients of {} exceed its own mass'.format(parent_nutrient_name))

    return nutrients_data
