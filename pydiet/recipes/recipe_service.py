from typing import TYPE_CHECKING, List, Optional
from heapq import nlargest
from datetime import datetime

from pyconsoleapp import search_tools

from pydiet.recipes.exceptions import (
    RecipeNotFoundError,
    TimeIntervalParseError,
    TimeIntervalValueError
)
from pydiet import repository_service as rps
from pydiet.recipes import recipe
from pydiet.ingredients import ingredient_amount

if TYPE_CHECKING:
    from pydiet.recipes.recipe import Recipe
    from pydiet.ingredients.ingredient_amount import IngredientAmount
    from pydiet.ingredients.ingredient import Ingredient


def load_new_recipe() -> 'Recipe':
    data_template = rps.read_recipe_template_data()
    return recipe.Recipe(data_template)


def load_recipe(datafile_name: str) -> 'Recipe':
    r_data = rps.read_recipe_data(datafile_name)
    return recipe.Recipe(r_data)


def save_new_recipe(recipe: 'Recipe') -> str:
    return rps.create_recipe_data(recipe._data)


def update_existing_recipe(recipe: 'Recipe', datafile_name: str) -> None:
    # Update the ingredient;
    rps.update_recipe_data(recipe._data, datafile_name)


def convert_recipe_name_to_datafile_name(recipe_name: str) -> str:
    # Load the index;
    index = rps.read_recipe_index()
    # Iterate through the index, searching for the filename;
    for datafile_name in index.keys():
        if index[datafile_name] == recipe_name:
            # Return the corresponding datafile name;
            return datafile_name
    # Raise an exception if none was found;
    raise RecipeNotFoundError

def get_matching_recipe_names(search_term: str, num_results: int) -> List[str]:
    # Load a list of the recipe names;
    index = rps.read_recipe_index()
    # Score each of the names against the search term;
    results = search_tools.score_similarity(list(index.values()), search_term)
    # Return the n largest scores;
    return nlargest(num_results, results, key=results.get)


def recipe_name_used(name: str, ignore_datafile: Optional[str] = None) -> bool:
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


def parse_time_interval(time_interval: str) -> str:
    # Split the string into two parts about the hyphen;
    start_and_end_time = time_interval.split('-')
    # Check there are two parts;
    if not len(start_and_end_time) == 2:
        raise TimeIntervalParseError
    # Try format the time into double digit 24hr format;
    try:
        for n, t in enumerate(start_and_end_time):
            d = datetime.strptime(t, "%H:%M")
            start_and_end_time[n] = d.strftime("%H:%M")
    except ValueError:
        raise TimeIntervalValueError
    # Check the intervals are not the same;
    if start_and_end_time[0] == start_and_end_time[1]:
        raise TimeIntervalValueError
    # Return the interval;
    return '-'.join(start_and_end_time)


def summarise_name(recipe: 'Recipe') -> str:
    if recipe.name:
        return recipe.name
    else:
        return 'Undefined'


def summarise_serve_intervals(recipe: 'Recipe') -> str:
    if len(recipe.serve_intervals):
        output = ''
        for se in recipe.serve_intervals:
            output = output+se+'\n'
        return output
    else:
        return 'No serve intervals added yet.\n'


def summarise_tags(recipe: 'Recipe') -> str:
    if len(recipe.tags):
        output = ''
        for cat in recipe.tags:
            output = output+'- {}\n'.format(cat)
        return output
    else:
        return 'No tags added yet.\n'


def summarise_ingredient_amount(ingredient_amount: 'IngredientAmount') -> str:
    _MAIN_INGRED_TEMPLATE = '{qty_template}{ingredient_name}{var_template}'
    _QTY_TEMPLATE = '{ingredient_qty}{ingredient_qty_units} of '
    _VAR_TEMPLATE = ' | between {qty_max}{ingredient_qty_units} and {qty_min}{ingredient_qty_units}'    
    output = ''
    # Build the qty string;
    if ingredient_amount.quantity:
        qty_template = _QTY_TEMPLATE.format(
            ingredient_qty=ingredient_amount.quantity, ingredient_qty_units=ingredient_amount.quantity_units)
    else:
        qty_template = 'Undefined amount of '
    # Build the var string;
    if ingredient_amount.quantity == None:
        var_template = ''
    elif ingredient_amount.perc_increase == 0 and ingredient_amount.perc_decrease == 0:
        var_template = ''
    else:
        var_template = _VAR_TEMPLATE.format(
            qty_max=ingredient_amount.max_quantity, qty_min=ingredient_amount.min_quantity,
            ingredient_qty_units=ingredient_amount.quantity_units)
    # Put everything together;
    output = output + _MAIN_INGRED_TEMPLATE.format(
        ingredient_name=ingredient_amount.name,
        qty_template=qty_template,
        var_template=var_template
    )
    return output

def summarise_steps(recipe: 'Recipe') -> str:
    if len(recipe.steps):
        output = '{} steps added.\n'.format(len(recipe.steps))
    else:
        output = 'No steps added yet.\n'
    return output
