from typing import TYPE_CHECKING, List, Optional
from heapq import nlargest

from pinjector import inject

from pydiet.ingredients.ingredient import Ingredient

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient, NutrientAmount
    from pydiet.shared import utility_service
    from pydiet.data import repository_service
    from pydiet.cli.ingredients.ingredient_edit_service import IngredientEditService

INGREDIENT_COST_SUMMARY_TEMPLATE = '£{cost:.2f} for {mass}{mass_units} (£{g_cost:.3f}/g)'
INGREDIENT_FLAG_SUMMARY_TEMPLATE = '{flag_name}: {status}'
NUTRIENT_SUMMARY_TEMPLATE = \
    '{nutrient_name}: {nutrient_mass}{nutrient_mass_units}/{ingredient_qty}{ingredient_qty_units}'
UNDEFINED_NUTRIENT_SUMMARY_TEMPLATE = '{nutrient_name}: Undefined'

def load_new_ingredient() -> 'Ingredient':
    rs: 'repository_service' = inject('pydiet.repository_service')
    data_template = rs.read_ingredient_template_data()
    return Ingredient(data_template)

def load_ingredient(datafile_name:str) -> 'Ingredient':
    rs: 'repository_service' = inject('pydiet.repository_service')
    i_data = rs.read_ingredient_data(datafile_name)
    return Ingredient(i_data)

def save_new_ingredient(ingredient: 'Ingredient') -> str:
    rs:'repository_service' = inject('pydiet.repository_service')
    return rs.create_ingredient_data(ingredient._data)

def update_existing_ingredient(ingredient:'Ingredient', datafile_name:str)->None:
    rs:'repository_service' = inject('pydiet.repository_service')
    rs.update_ingredient_data(ingredient._data, datafile_name)

def resolve_ingredient_datafile_name(ingredient_name:str)->Optional[str]:
    # Grab reference to repository service;
    rp:'repository_service' = inject('pydiet.repository_service')
    # Load the index;
    index = rp.read_ingredient_index()
    # Iterate through the index, searching for filename;
    for datafile_name in index.keys():
        if index[datafile_name] == ingredient_name:
            # Return corresponding datafile name;
            return datafile_name
    # Return None if name was not found;
    return None


def resolve_nutrient_alias(alias: str) -> str:
    configs: 'configs' = inject('pydiet.configs')
    # Hunt through the alias list and return rootname
    # if match is found;
    for rootname in configs.NUTRIENT_ALIASES.keys():
        if alias in configs.NUTRIENT_ALIASES[rootname]:
            return rootname
    # Not found, just return;
    return alias

def get_matching_ingredient_names(search_term:str, num_results: int) -> List[str]:
    # Load in dependencies;
    rp:'repository_service' = inject('pydiet.repository_service')
    ut: 'utility_service' = inject('pydiet.utility_service')
    # Load a list of the ingredient names;
    index = rp.read_ingredient_index()
    # Score each of the names against the search term;
    results = ut.score_similarity(list(index.values()), search_term)
    # Return the n largest scores;
    return nlargest(num_results, results, key=results.get)

def get_matching_nutrient_names(search_term: str, num_results: int) -> List[str]:
    # Load the ingredient template datafile;
    rs: 'repository_service' = inject('pydiet.repository_service')
    template = rs.read_ingredient_template_data()
    # Score each of the nutrient names against the search term;
    ut: 'utility_service' = inject('pydiet.utility_service')
    results = ut.score_similarity(
        list(template['nutrients'].keys()), search_term)
    return nlargest(num_results, results, key=results.get)

def ingredient_name_used(name:str, ignore_datafile:Optional[str]=None)->bool:
    # Grab some references we need;
    rp:'repository_service' = inject('pydiet.repository_service')
    # Load the index data;
    index = rp.read_ingredient_index()
    # If we are ignoring a datafile, drop it;
    if ignore_datafile:
        index.pop(ignore_datafile)
    # If we are editing an ingredient, pop its name from the datafile
    if name in index.values():
        return True
    else:
        return False

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
