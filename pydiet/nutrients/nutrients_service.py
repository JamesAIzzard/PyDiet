from heapq import nlargest
from typing import List, Dict, TYPE_CHECKING

from pyconsoleapp import search_tools

from pydiet import nutrients

if TYPE_CHECKING:
    from pydiet.nutrients.supports_nutrients import NutrientData

def all_primary_and_alias_nutrient_names() -> List[str]:
    '''Returns a list of every nutrient name and alias registered to the system.
    Note: All aliases are returned, so names may refer to the same nutrient.

    Returns:
        List[str]: List of all registered nutrient names.
    '''
    names = []
    for nutrient_name in nutrients.configs.all_primary_nutrient_names:
        names.append(nutrient_name)
    for nutrient_aliases in nutrients.configs.nutrient_aliases.values():
        for alias in nutrient_aliases:
            names.append(alias)
    return names


def validate_nutrient_name(name: str) -> str:
    '''Checks a nutrient name is real. 
    - Replaces whitespace with underscore if whitespace is in the name. 
    - Raises an exception if name is unknown.

    Args:
        name (str): Name to validate.

    Raises:
        nutrients.exceptions.UnknownNutrientNameError: If name is not
            recognised.

    Returns:
        str: Validated name.
    '''
    name = name.replace(' ', '_')
    # Just return if all OK;
    if name in all_primary_and_alias_nutrient_names():
        return name
    # Wasn't found, so raise an exception;
    raise nutrients.exceptions.UnknownNutrientNameError


def get_nutrient_primary_name(nutrient_name: str) -> str:
    '''Returns the primary name corresponding to any known
    nutrient name.

    Args:
        alias (str): Name to lookup the primary name for.

    Raises:
        nutrients.exceptions.UnknownNutrientNameError

    Returns:
        str: Primary nutrient name corresponding to the
            nutrient name provided.
    '''
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
    raise nutrients.exceptions.UnknownNutrientNameError


def get_matching_nutrient_names(search_term: str, num_results: int) -> List[str]:
    '''Finds a max of n nutrient names most similar to the search term provided.

    Args:
        search_term (str): Name to search for.
        num_results (int): Max number of names to return.

    Returns:
        List[str]: Nutrient names closest to search term.
    '''
    # Score each of the nutrient names against the search term;
    results = search_tools.score_similarity(
        all_primary_and_alias_nutrient_names(), search_term)
    return nlargest(num_results, results, key=results.get)

def validate_nutritients_data(data:Dict[str, 'NutrientData']) -> None:
    raise NotImplementedError

# def print_nutrient_targets_menu(subject: 'nutrients.i_has_nutrient_targets.IHasNutrientTargets') -> str:
#     output = ''
#     if len(subject.nutrient_targets):
#         for i, nutrient_name in enumerate(subject.nutrient_targets.keys(), start=1):
#             output = output + '{num}. {nutrient_name} - {nutrient_qty}{nutrient_qty_units}'.format(
#                 num=i,
#                 nutrient_name=nutrient_name,
#                 nutrient_qty=subject.nutrient_targets[nutrient_name][0],
#                 nutrient_qty_units=subject.nutrient_targets[nutrient_name][1])
#     else:
#         output = 'No nutrient targets assigned.'
#     return output

# def print_nutrient_amount_summary(nutrient_amount: 'nutrients.nutrient_amount.NutrientAmount') -> str:
#     # Define the templates;
#     defined_nutrient_template = '{nutrient_name}: {nutrient_mass}{nutrient_mass_units}/{ingredient_qty}{ingredient_qty_units}'
#     undefined_nutrient_template = '{nutrient_name}: Undefined'

#     if nutrient_amount.defined:
#         perc = nutrient_amount.percentage
#         perc_insert = ' (none)'
#         if perc > 0 and perc < 0.01:
#             perc_insert = ' (trace)'
#         elif perc > 0.01:
#             perc_insert = ' ({:.3f})%'.format(perc)
#         return defined_nutrient_template.format(
#             nutrient_name=nutrient_amount.name.replace('_', ' '),
#             nutrient_mass=nutrient_amount.nutrient_mass,
#             nutrient_mass_units=nutrient_amount.nutrient_mass_units,
#             ingredient_qty=nutrient_amount.ingredient_qty,
#             ingredient_qty_units=nutrient_amount.ingredient_qty_units,
#         ) + perc_insert
#     else:
#         return undefined_nutrient_template.format(
#             nutrient_name=nutrient_amount.name.replace('_', ' ')
#         )
