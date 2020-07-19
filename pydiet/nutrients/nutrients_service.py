from heapq import nlargest
from typing import List

from pyconsoleapp import search_tools

from pydiet import nutrients

def resolve_nutrient_alias(alias: str) -> str:
    # Hunt through the alias list and return rootname
    # if match is found;
    for rootname in nutrients.configs.NUTRIENT_ALIASES.keys():
        if alias in nutrients.configs.NUTRIENT_ALIASES[rootname]:
            return rootname
    # Not found, just return;
    return alias

def get_matching_nutrient_names(search_term: str, num_results: int) -> List[str]:
    # Score each of the nutrient names against the search term;
    results = search_tools.score_similarity(
        nutrients.configs.NUTRIENTS, search_term)
    return nlargest(num_results, results, key=results.get)

def print_nutrient_targets_menu(subject: 'nutrients.i_has_nutrient_targets.IHasNutrientTargets') -> str:
    output = ''
    if len(subject.nutrient_targets):
        for i, nutrient_name in enumerate(subject.nutrient_targets.keys(), start=1):
            output = output + '{num}. {nutrient_name} - {nutrient_qty}{nutrient_qty_units}'.format(
                num=i,
                nutrient_name=nutrient_name,
                nutrient_qty=subject.nutrient_targets[nutrient_name][0],
                nutrient_qty_units=subject.nutrient_targets[nutrient_name][1])
    else:
        output = 'No nutrient targets assigned.'
    return output

def print_nutrient_amount_summary(nutrient_amount: 'nutrients.nutrient_amount.NutrientAmount') -> str:
    # Define the templates;
    defined_nutrient_template = '{nutrient_name}: {nutrient_mass}{nutrient_mass_units}/{ingredient_qty}{ingredient_qty_units}'
    undefined_nutrient_template = '{nutrient_name}: Undefined'
    
    if nutrient_amount.defined:
        perc = nutrient_amount.percentage
        perc_insert = ' (none)'
        if perc > 0 and perc < 0.01:
            perc_insert = ' (trace)'
        elif perc > 0.01:
            perc_insert = ' ({:.3f})%'.format(perc)
        return defined_nutrient_template.format(
            nutrient_name=nutrient_amount.name.replace('_', ' '),
            nutrient_mass=nutrient_amount.nutrient_mass,
            nutrient_mass_units=nutrient_amount.nutrient_mass_units,
            ingredient_qty=nutrient_amount.ingredient_qty,
            ingredient_qty_units=nutrient_amount.ingredient_qty_units,
        ) + perc_insert
    else:
        return undefined_nutrient_template.format(
            nutrient_name=nutrient_amount.name.replace('_', ' ')
        )    