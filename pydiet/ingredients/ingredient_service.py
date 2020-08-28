from pydiet.quantity import quantity_service
from typing import TYPE_CHECKING, List, Optional
from heapq import nlargest

from pyconsoleapp import search_tools

from pydiet import ingredients, repository, flags, nutrients, cost, quantity


if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient


def load_new_ingredient() -> 'Ingredient':
    # Initialise the data template;
    data_template = ingredients.ingredient.data_template
    # Add the costs;
    data_template['cost_per_mass'] = cost.i_has_cost.data_template
    # Add the flags;
    for flag in flags.configs.all_flag_names:
        data_template['flags'][flag] = None
    # Add the nutrients;
    for nutrient_name in nutrients.configs.all_nutrient_names:
        data_template['nutrients'][nutrient_name] = nutrients.nutrient_amount.data_template
    # Add the density;
    data_template['vol_density'] = quantity.i_has_density.data_template

    # Init and return the ingredient;
    return ingredients.ingredient.Ingredient(data_template)


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


def ingredient_name_taken(name: str, ignore_datafile: Optional[str] = None) -> bool:
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