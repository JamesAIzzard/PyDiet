from typing import TYPE_CHECKING, List, Optional
from heapq import nlargest

from pydiet.recipes.exceptions import RecipeNotFoundError

from pydiet.data import repository_service as rps
from pydiet.shared import utility_service as uts
from pydiet.recipes import recipe

if TYPE_CHECKING:
    from pydiet.recipes.recipe import Recipe

def load_new_recipe() -> 'Recipe':
    data_template = rps.read_recipe_template_data()
    return recipe.Recipe(data_template)

def load_recipe(datafile_name:str) -> 'Recipe':
    r_data = rps.read_recipe_data(datafile_name)
    return recipe.Recipe(r_data)

def save_new_recipe(recipe: 'Recipe') -> str:
    return rps.create_recipe_data(recipe._data)

def update_existing_recipe(recipe:'Recipe', datafile_name:str)->None:
    # Update the ingredient;
    rps.update_recipe_data(recipe._data, datafile_name)

def resolve_recipe_datafile_name(recipe_name:str) -> str:
    # Load the index;
    index = rps.read_recipe_index()
    # Iterate through the index, searching for the filename;
    for datafile_name in index.keys():
        if index[datafile_name] == recipe_name:
            # Return the corresponding datafile name;
            return datafile_name
    # Raise an exception if none was found;
    raise RecipeNotFoundError

def get_matching_recipe_names(search_term:str, num_results:int) -> List[str]:
    # Load a list of the recipe names;
    index = rps.read_recipe_index()
    # Score each of the names against the search term;
    results = uts.score_similarity(list(index.values()), search_term)
    # Return the n largest scores;
    return nlargest(num_results, results, key=results.get)

def recipe_name_used(name:str, ignore_datafile:Optional[str]=None)->bool:
    # Bring the name list in;
    index = rps.read_recipe_index()
    # If we are ignoring a datafile, then drop it;
    if ignore_datafile:
        index.pop(ignore_datafile)
    # Return the status;
    if name in index.values():
        return True
    else:
        return False

def summarise_name(recipe:'Recipe') -> str:
    if recipe.name:
        return recipe.name
    else:
        return 'Undefined'

def summarise_serve_intervals(recipe:'Recipe') -> str:
    if len(recipe.serve_intervals):
        output = ''
        for se in recipe.serve_intervals:
            output = output+se+'\n'
        return output
    else:
        return 'No serve intervals added yet.\n'

def summarise_categories(recipe:'Recipe') -> str:
    if len(recipe.categories):
        output = ''
        for cat in recipe.categories:
            output = output+cat+'\n'
        return output
    else:
        return 'No categories added yet.\n'

def summarise_ingredients(recipe:'Recipe') -> str:
    if len(recipe.ingredient_amounts):
        output = ''
        for ie in recipe.ingredient_amounts.values():
            output = output + '{name}: +{perc_inc}%/-{perc_dec}%\n'.format(
                name=ie.ingredient.name,
                perc_inc=ie.perc_increase,
                perc_dec=ie.perc_decrease
            )
        return output
    else:
        return 'No ingredients added yet.\n'    