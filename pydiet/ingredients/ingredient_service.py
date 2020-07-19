from typing import TYPE_CHECKING, List, Optional
from heapq import nlargest

from pyconsoleapp import search_tools

from pydiet import ingredients, repository, flags, nutrients


if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient


INGREDIENT_COST_SUMMARY_TEMPLATE = '£{cost:.2f} for {mass}{mass_units} (£{g_cost:.3f}/g)'
INGREDIENT_FLAG_SUMMARY_TEMPLATE = '{flag_name}: {status}'


def load_new_ingredient() -> 'Ingredient':
    # Initialise the data template;
    dt = ingredients.ingredient.DATA_TEMPLATE
    # Add the flags;
    for flag in flags.configs.FLAGS:
        dt['flags'][flag] = None
    # Add the nutrients;
    for nutrient in nutrients.configs.NUTRIENTS:
        dt['nutrients'][nutrient] = nutrients.nutrient_amount.DATA_TEMPLATE

    # Init and return the ingredient;
    return ingredients.ingredient.Ingredient(dt)


def load_ingredient(datafile_name: str) -> 'Ingredient':
    i_data = repository.repository_service.read_ingredient_data(datafile_name)
    return ingredients.ingredient.Ingredient(i_data)


def save_new_ingredient(ingredient: 'Ingredient') -> str:
    return repository.repository_service.create_ingredient_data(ingredient._data)


def update_existing_ingredient(ingredient: 'Ingredient', datafile_name: str) -> None:
    # Update the ingredient;
    repository.repository_service.update_ingredient_data(
        ingredient._data, datafile_name)


def convert_ingredient_name_to_datafile_name(ingredient_name: str) -> str:
    # Load the index;
    index = repository.repository_service.read_ingredient_index()
    # Iterate through the index, searching for filename;
    for datafile_name in index.keys():
        if index[datafile_name] == ingredient_name:
            # Return corresponding datafile name;
            return datafile_name
    # Raise exception if none was found;
    raise ingredients.exceptions.IngredientNotFoundError


def convert_datafile_name_to_ingredient_name(datafile_name: str) -> str:
    # Load the index;
    index = repository.repository_service.read_ingredient_index()
    # Return the name associated with the datafile name;
    if datafile_name in index.keys():
        return index[datafile_name]
    else:
        raise ingredients.exceptions.IngredientNotFoundError


def get_matching_ingredient_names(search_term: str, num_results: int) -> List[str]:
    # Load a list of the ingredient names;
    index = repository.repository_service.read_ingredient_index()
    # Score each of the names against the search term;
    results = search_tools.score_similarity(list(index.values()), search_term)
    # Return the n largest scores;
    return nlargest(num_results, results, key=results.get)


def ingredient_name_used(name: str, ignore_datafile: Optional[str] = None) -> bool:
    # Load the index data;
    index = repository.repository_service.read_ingredient_index()
    # If we are ignoring a datafile, drop it;
    if ignore_datafile:
        index.pop(ignore_datafile)
    # Return the status;
    if name in index.values():
        return True
    else:
        return False


def summarise_status(ingredient: 'Ingredient') -> str:
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


def summarise_density(ingredient: 'Ingredient') -> str:
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


def summarise_flag(ingredient: 'Ingredient', flag_name: str) -> str:
    flag = ingredient.get_flag(flag_name)
    if flag == None:
        flag = 'Undefined'
    return '{}: {}'.format(
        flag_name.replace('_', ' '),
        flag
    )
