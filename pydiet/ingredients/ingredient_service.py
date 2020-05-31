from typing import TYPE_CHECKING, List, Optional
from heapq import nlargest

from pyconsoleapp import search_tools

from pydiet.ingredients import ingredient
from pydiet.ingredients.exceptions import (
    IngredientNotFoundError
)
from pydiet import repository_service as rps
from pydiet import configs as cfg

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import NutrientAmount
    from pydiet.ingredients.ingredient import Ingredient


INGREDIENT_COST_SUMMARY_TEMPLATE = '£{cost:.2f} for {mass}{mass_units} (£{g_cost:.3f}/g)'
INGREDIENT_FLAG_SUMMARY_TEMPLATE = '{flag_name}: {status}'
NUTRIENT_SUMMARY_TEMPLATE = \
    '{nutrient_name}: {nutrient_mass}{nutrient_mass_units}/{ingredient_qty}{ingredient_qty_units}'
UNDEFINED_NUTRIENT_SUMMARY_TEMPLATE = '{nutrient_name}: Undefined'

def load_new_ingredient() -> 'Ingredient':
    data_template = rps.read_ingredient_template_data()
    return ingredient.Ingredient(data_template)

def load_ingredient(datafile_name:str) -> 'Ingredient':
    i_data = rps.read_ingredient_data(datafile_name)
    return ingredient.Ingredient(i_data)

def save_new_ingredient(ingredient: 'Ingredient') -> str:
    return rps.create_ingredient_data(ingredient._data)

def update_existing_ingredient(ingredient:'Ingredient', datafile_name:str)->None:
    # Update the ingredient;
    rps.update_ingredient_data(ingredient._data, datafile_name)

def resolve_ingredient_datafile_name(ingredient_name:str)->str:
    # Load the index;
    index = rps.read_ingredient_index()
    # Iterate through the index, searching for filename;
    for datafile_name in index.keys():
        if index[datafile_name] == ingredient_name:
            # Return corresponding datafile name;
            return datafile_name
    # Raise exception if none was found;
    raise IngredientNotFoundError

def resolve_nutrient_alias(alias: str) -> str:
    # Hunt through the alias list and return rootname
    # if match is found;
    for rootname in cfg.NUTRIENT_ALIASES.keys():
        if alias in cfg.NUTRIENT_ALIASES[rootname]:
            return rootname
    # Not found, just return;
    return alias

def get_all_nutrient_names() -> List[str]:
    data_template = rps.read_ingredient_template_data()
    return list(data_template['nutrients'].keys())

def get_matching_ingredient_names(search_term:str, num_results: int) -> List[str]:
    # Load a list of the ingredient names;
    index = rps.read_ingredient_index()
    # Score each of the names against the search term;
    results = search_tools.score_similarity(list(index.values()), search_term)
    # Return the n largest scores;
    return nlargest(num_results, results, key=results.get)

def get_matching_nutrient_names(search_term: str, num_results: int) -> List[str]:
    template = rps.read_ingredient_template_data()
    # Score each of the nutrient names against the search term;
    results = search_tools.score_similarity(
        list(template['nutrients'].keys()), search_term)
    return nlargest(num_results, results, key=results.get)

def ingredient_name_used(name:str, ignore_datafile:Optional[str]=None)->bool:
    # Load the index data;
    index = rps.read_ingredient_index()
    # If we are ignoring a datafile, drop it;
    if ignore_datafile:
        index.pop(ignore_datafile)
    # Return the status;
    if name in index.values():
        return True
    else:
        return False

def summarise_status(ingredient:'Ingredient')->str:
    if ingredient.defined:
        return 'Complete'
    else:
        return 'Incomplete, requires {}'.format(ingredient.missing_mandatory_attrs[0])

def summarise_name(ingredient: 'Ingredient') -> str:
    if ingredient.name:
        return ingredient.name
    else:
        return 'Undefined'


def summarise_cost(ingredient: 'Ingredient') -> str:
    if ingredient.cost_is_defined:
        cost_data = ingredient.cost_data
        return INGREDIENT_COST_SUMMARY_TEMPLATE.format(
            cost=cost_data['cost'],
            mass=cost_data['ingredient_qty'],
            mass_units=cost_data['ingredient_qty_units'],
            g_cost=ingredient.cost_per_g
        )
    else:
        return 'Undefined'

def summarise_density(ingredient:'Ingredient')->str:
    if ingredient.density_is_defined:
        return '{ingredient_mass}{ingredient_mass_units}/{ingredient_vol}{ingredient_vol_units} ({density_g_ml}g/ml)'.format(
            ingredient_mass=ingredient._data['vol_density']['ingredient_mass'],
            ingredient_mass_units=ingredient._data['vol_density']['ingredient_mass_units'],
            ingredient_vol=ingredient._data['vol_density']['ingredient_vol'],
            ingredient_vol_units=ingredient._data['vol_density']['ingredient_vol_units'],
            density_g_ml=ingredient.density_g_per_ml
        )
    else:
        return 'Undefined'

def summarise_flag(ingredient:'Ingredient', flag_name:str) -> str:
    flag = ingredient.get_flag(flag_name)
    if flag == None:
        flag = 'Undefined'
    return '{}: {}'.format(
        flag_name.replace('_', ' '),
        flag
    )

def summarise_nutrient_amount(nutrient_amount: 'NutrientAmount') -> str:
    if nutrient_amount.defined:
        perc = nutrient_amount.percentage
        perc_insert = ' (none)'
        if perc > 0 and perc < 0.01:
            perc_insert = ' (trace)'
        elif perc > 0.01:
            perc_insert = ' ({:.3f})%'.format(perc)
        return NUTRIENT_SUMMARY_TEMPLATE.format(
            nutrient_name=nutrient_amount.name.replace('_', ' '),
            nutrient_mass=nutrient_amount.nutrient_mass,
            nutrient_mass_units=nutrient_amount.nutrient_mass_units,
            ingredient_qty=nutrient_amount.ingredient_qty,
            ingredient_qty_units=nutrient_amount.ingredient_qty_units,
        ) + perc_insert
    else:
        return UNDEFINED_NUTRIENT_SUMMARY_TEMPLATE.format(
            nutrient_name=nutrient_amount.name.replace('_', ' ')
        )
