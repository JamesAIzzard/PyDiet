from typing import TYPE_CHECKING, List
from heapq import nlargest

from pinjector import inject

from pydiet.ingredients.ingredient import Ingredient

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient, NutrientAmount
    from pydiet import utility_service
    from pydiet.data import repository_service
    from pydiet import configs

INGREDIENT_COST_SUMMARY_TEMPLATE = '£{cost:.2f} for {mass}{mass_units} (£{g_cost:.3f}/g)'
INGREDIENT_FLAG_SUMMARY_TEMPLATE = '{flag_name}: {status}'
NUTRIENT_SUMMARY_TEMPLATE = \
    '{nutrient_name}: {nutrient_mass}{nutrient_mass_units}/{ingredient_mass}{ingredient_mass_units}'
UNDEFINED_NUTRIENT_SUMMARY_TEMPLATE = '{nutrient_name}: Undefined'

def resolve_alias(alias: str) -> str:
    configs: 'configs' = inject('pydiet.configs')
    # Hunt through the alias list and return rootname
    # if match is found;
    for rootname in configs.NUTRIENT_ALIASES.keys():
        if alias in configs.NUTRIENT_ALIASES[rootname]:
            return rootname
    # Not found, just return;
    return alias


def get_new_ingredient() -> 'Ingredient':
    rs: 'repository_service' = inject('pydiet.repository_service')
    data_template = rs.read_ingredient_data_template()
    return Ingredient(data_template)


def get_matching_nutrient_names(search_term: str, num_results: int) -> List[str]:
    # Load the ingredient template datafile;
    rs: 'repository_service' = inject('pydiet.repository_service')
    template = rs.read_ingredient_data_template()
    # Score each of the nutrient names against the search term;
    ut: 'utility_service' = inject('pydiet.utility_service')
    results = ut.score_similarity(
        list(template['nutrients'].keys()), search_term)
    return nlargest(num_results, results, key=results.get)


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
            mass=cost_data['ingredient_mass'],
            mass_units=cost_data['ingredient_mass_units'],
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
        perc_insert = ' (trace)'
        if perc > 0.01:
            perc_insert = ' ({:.3f})%'.format(perc)
        return NUTRIENT_SUMMARY_TEMPLATE.format(
            nutrient_name=nutrient_amount.name.replace('_', ' '),
            nutrient_mass=nutrient_amount.nutrient_mass,
            nutrient_mass_units=nutrient_amount.nutrient_mass_units,
            ingredient_mass=nutrient_amount.ingredient_mass,
            ingredient_mass_units=nutrient_amount.ingredient_mass_units,
        ) + perc_insert
    else:
        return UNDEFINED_NUTRIENT_SUMMARY_TEMPLATE.format(
            nutrient_name=nutrient_amount.name.replace('_', ' ')
        )
