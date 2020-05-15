from typing import TYPE_CHECKING, List, Optional
from heapq import nlargest

from pinjector import inject

from pydiet.recipes.recipe import Recipe
from pydiet.recipes.exceptions import RecipeNotFoundError

if TYPE_CHECKING:
    from pydiet.data import repository_service
    from pydiet.shared import utility_service
    from pydiet.recipes.recipe import Recipe

def load_new_recipe() -> 'Recipe':
    _rs:'repository_service' = inject('pydiet.repository_service')
    data_template = _rs.read_recipe_template_data()
    return Recipe(data_template)

def load_recipe(datafile_name:str) -> 'Recipe':
    _rs:'repository_service' = inject('pydiet.repository_service')
    r_data = _rs.read_recipe_data(datafile_name)
    return Recipe(r_data)

def save_new_recipe(recipe: 'Recipe') -> str:
    _rs:'repository_service' = inject('pydiet.repository_service')
    return _rs.create_recipe_data(recipe._data)

def update_existing_recipe(recipe:'Recipe', datafile_name:str)->None:
    _rs:'repository_service' = inject('pydiet.repository_service')
    # Update the ingredient;
    _rs.update_recipe_data(recipe._data, datafile_name)

def resolve_recipe_datafile_name(recipe_name:str) -> str:
    _rs:'repository_service' = inject('pydiet.repository_service')
    # Load the index;
    index = _rs.read_recipe_index()
    # Iterate through the index, searching for the filename;
    for datafile_name in index.keys():
        if index[datafile_name] == recipe_name:
            # Return the corresponding datafile name;
            return datafile_name
    # Raise an exception if none was found;
    raise RecipeNotFoundError

def get_matching_recipe_names(search_term:str, num_results:int) -> List[str]:
    _rs:'repository_service' = inject('pydiet.repository_service')
    _ut:'utility_service' = inject('pydiet.utility_service')
    # Load a list of the recipe names;
    index = _rs.read_recipe_index()
    # Score each of the names against the search term;
    results = _ut.score_similarity(list(index.values()), search_term)
    # Return the n largest scores;
    return nlargest(num_results, results, key=results.get)

def recipe_name_used(name:str, ignore_datafile:Optional[str]=None)->bool:
    _rs:'repository_service' = inject('pydiet.repository_service')
    # Bring the name list in;
    index = _rs.read_recipe_index()
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