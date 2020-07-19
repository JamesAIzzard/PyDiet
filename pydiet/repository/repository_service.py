from typing import Dict, Callable
import json, uuid, os

from pydiet import configs, ingredients, recipes, goals, repository

def _create_indexed_datafile(data: Dict,
                             read_index_func: Callable,
                             update_index_func: Callable) -> str:
    '''Writes a datadict to a new datafile on the disk.

    Args:
        data (Dict): The data dictionary to write.
        read_index_func (Callable): Function to return the relevant index as a dict.
        update_index_func (Callable): Function to update the relevant index on disk.

    Raises:
        DatafileNameUndefinedError: [description]
        DuplicateDatafileNameError: [description]

    Returns:
        str: The datafile's filename on disk.
    '''
    # Check the 'name' field in the datafile is populated;
    if not data['name']:
        raise repository.exceptions.DatafileNameUndefinedError
    # Check the 'name' field in the datafile is unique;
    index = read_index_func()
    if data['name'] in index.values():
        raise repository.exceptions.DuplicateDatafileNameError
    
    # Create the unique filename;
    filename = str(uuid.uuid4())
    filename_w_ext = filename+'.json'

    # Update the index with the filename;
    index[filename] = data['name']
    update_index_func(index)

    # Write the ingredient datafile;
    with open(filename_w_ext, 'w') as fh:
        json.dump(data, fh, indent=2, sort_keys=True)

    # Return the filename;
    return filename

def _read_json_datafile(filepath:str) -> Dict:
    '''Reads a .json datafile and returns as a dict.

    Args:
        filepath (str): Filepath to .json file, including filename and ext.

    Returns:
        Dict: The contents of the datafile as a dict.
    '''
    # Read the datafile contents;
    with open(filepath, 'r') as fh:
        raw_data = fh.read()
        # Parse into dict;
        data = json.loads(raw_data)
        # Return it;
        return data  

def create_ingredient_data(ingredient_data: Dict) -> str:
    '''Writes an ingredient data dict to a new ingredient
    datafile on disk.

    Args:
        ingredient_data (Dict): Ingredient data dictionary.

    Returns:
        str: The filename for the ingredient datafile on disk.
    '''
    return _create_indexed_datafile(ingredient_data, read_ingredient_index, update_ingredient_index)


def create_recipe_data(recipe_data: Dict) -> str:
    '''Writes an recipe data dict to a new recipe
    datafile on disk.

    Args:
        recipe_data (Dict): Recipe data dictionary.

    Returns:
        str: The filename for the recipe datafile on disk.
    '''    
    return _create_indexed_datafile(recipe_data, read_recipe_index, update_recipe_index)


def create_day_goals_data(day_goals_data: Dict) -> str:
    '''Writes an daygoals data dict to a new daygoals
    datafile on disk.

    Args:
        day_goals_data (Dict): DayGoals data dictionary.

    Returns:
        str: The filename for the daygoals datafile on disk.
    '''
    return _create_indexed_datafile(day_goals_data, read_day_goals_index, update_day_goals_index)  

def read_ingredient_data(ingredient_datafile_name: str) -> Dict:
    '''Returns an ingredient datafile as a dict.

    Args:
        ingredient_datafile_name (str): Filename of ingredient
            datafile, without the extension.

    Returns:
        Dict: Ingredient datafile in dictionary format.
    '''
    return _read_json_datafile('{path_to}+{filename}.json'.format(
        path_to=configs.INGREDIENT_DB_PATH,
        filename=ingredient_datafile_name
    ))


def read_recipe_data(recipe_datafile_name: str) -> Dict:
    '''Returns an recipe datafile as a dict.

    Args:
        recipe_datafile_name (str): Filename of recipe
            datafile, without the extension.

    Returns:
        Dict: recipe datafile in dictionary format.
    '''
    return _read_json_datafile('{path_to}+{filename}.json'.format(
        path_to=configs.RECIPE_DB_PATH,
        filename=recipe_datafile_name
    ))


def read_day_goals_data(day_goals_datafile_name: str) -> Dict:
    '''Returns an day goals datafile as a dict.

    Args:
        day_goals_datafile_name (str): Filename of day goals
            datafile, without the extension.

    Returns:
        Dict: day goals datafile in dictionary format.
    '''
    return _read_json_datafile('{path_to}+{filename}.json'.format(
        path_to=configs.DAY_GOALS_DB_PATH,
        filename=day_goals_datafile_name
    ))


def read_global_day_goals_data() -> Dict:
    '''Returns the saved global day goals data as a dict.

    Returns:
        Dict: Global day goals data.
    '''
    return _read_json_datafile(configs.GLOBAL_DAY_GOALS_DB_PATH)


def read_ingredient_index() -> Dict[str, str]:
    '''Returns the saved ingredient index as a dict;

    Returns:
        Dict[str, str]: The saved ingredients index.
    '''
    return _read_json_datafile('{ingredient_db_path}{index_name}.json'.format(
        ingredient_db_path=configs.INGREDIENT_DB_PATH,
        index_name=configs.INGREDIENT_INDEX_NAME
    ))


def read_recipe_index() -> Dict[str, str]:
    '''Returns the saved recipe index as a dict;

    Returns:
        Dict[str, str]: The saved recipe index.
    '''
    return _read_json_datafile('{recipe_db_path}{index_name}.json'.format(
        recipe_db_path=configs.RECIPE_DB_PATH,
        index_name=configs.RECIPE_INDEX_NAME
    ))


def read_day_goals_index() -> Dict[str, str]:
    with open(configs.DAY_GOALS_DB_PATH+'{}.json'.
              format(configs.DAY_GOALS_INDEX_NAME)) as fh:
        raw_data = fh.read()
        data = json.loads(raw_data)
        return data


def update_ingredient_data(ingredient_data: Dict, datafile_name: str) -> None:
    # Load the index to do some checks;
    index = read_ingredient_index()
    # Check the ingredient name is populated;
    if not ingredient_data['name']:
        raise ingredients.exceptions.IngredientNameUndefinedError
    # Check the ingredient name is not used by another datafile;
    # Pop the current name, because if it hasn't changed, we don't want to
    # detect it;
    index.pop(datafile_name)
    # Now current has been removed, check everwhere else for name;
    if ingredient_data['name'] in index.values():
        raise ingredients.exceptions.DuplicateIngredientNameError(
            'Another ingredient already uses the name {}'.format(ingredient_data['name']))
    # Write the ingredient data;
    with open(configs.INGREDIENT_DB_PATH+datafile_name+'.json', 'w') as fh:
        json.dump(ingredient_data, fh, indent=2, sort_keys=True)
    # Update the index;
    index[datafile_name] = ingredient_data['name']
    update_ingredient_index(index)


def update_recipe_data(recipe_data: Dict, datafile_name: str) -> None:
    # Load the index to do some checks;
    index = read_recipe_index()
    # Check the recipe name is populated;
    if not recipe_data['name']:
        raise recipes.exceptions.RecipeNameUndefinedError
    # Check the recipe name is not used by another datafile;
    # Pop the current name, because if it hasn't changed, we don't want to
    # detect it;
    index.pop(datafile_name)
    # Now current has been removed, check everwhere else for name;
    if recipe_data['name'] in index.values():
        raise recipes.exceptions.DuplicateRecipeNameError(
            'Another recipe already uses the name {}'.format(recipe_data['name']))
    # Write the recipe data;
    with open(configs.RECIPE_DB_PATH+datafile_name+'.json', 'w') as fh:
        json.dump(recipe_data, fh, indent=2, sort_keys=True)
    # Update the index;
    index[datafile_name] = recipe_data['name']
    update_recipe_index(index)


def update_day_goals_data(day_goals_data: Dict, datafile_name: str) -> None:
    # Load the index to do some checks;
    index = read_day_goals_index()
    # Check the day_goals name is populated;
    if not day_goals_data['name']:
        raise goals.exceptions.DayGoalsNameUndefinedError
    # Check the day_goals name is not used by another datafile;
    # Pop the current name, because if it hasn't changed, we don't want to
    # detect it;
    index.pop(datafile_name)
    # Now current has been removed, check everwhere else for name;
    if day_goals_data['name'] in index.values():
        raise goals.exceptions.DuplicateDayGoalsNameError(
            'Another day already uses the name {}'.format(day_goals_data['name']))
    # Write the day_goals data;
    with open(configs.DAY_GOALS_DB_PATH+datafile_name+'.json', 'w') as fh:
        json.dump(day_goals_data, fh, indent=2, sort_keys=True)
    # Update the index;
    index[datafile_name] = day_goals_data['name']
    update_day_goals_index(index)


def update_global_day_goals_data(global_day_goals_data: Dict) -> None:
    # Write the data;
    with open(configs.GLOBAL_DAY_GOALS_DB_PATH, 'w') as fh:
        json.dump(global_day_goals_data, fh, indent=2, sort_keys=True)


def update_ingredient_index(index: Dict[str, str]) -> None:
    with open(configs.INGREDIENT_DB_PATH+'{}.json'.
              format(configs.INGREDIENT_INDEX_NAME), 'w') as fh:
        json.dump(index, fh, indent=2, sort_keys=True)


def update_recipe_index(index: Dict[str, str]) -> None:
    with open(configs.RECIPE_DB_PATH+'{}.json'.
              format(configs.RECIPE_INDEX_NAME), 'w') as fh:
        json.dump(index, fh, indent=2, sort_keys=True)


def update_day_goals_index(index: Dict[str, str]) -> None:
    with open(configs.DAY_GOALS_DB_PATH+'{}.json'.
              format(configs.DAY_GOALS_INDEX_NAME), 'w') as fh:
        json.dump(index, fh, indent=2, sort_keys=True)


def delete_ingredient_data(datafile_name: str) -> None:
    # Open the index;
    index = read_ingredient_index()
    # Remove the entry from the index;
    index.pop(datafile_name)
    # Rewrite the index;
    update_ingredient_index(index)
    # Delete the datafile;
    os.remove(configs.INGREDIENT_DB_PATH+datafile_name+'.json')


def delete_recipe_data(datafile_name: str) -> None:
    # Open the index;
    index = read_recipe_index()
    # Remove the entry from the index;
    index.pop(datafile_name)
    # Rewrite the index;
    update_recipe_index(index)
    # Delete the datafile;
    os.remove(configs.RECIPE_DB_PATH+datafile_name+'.json')


def delete_day_goals_data(datafile_name: str) -> None:
    # Open the index;
    index = read_day_goals_index()
    # Remove the entry from the index;
    index.pop(datafile_name)
    # Rewrite the index;
    update_day_goals_index(index)
    # Delete the datafile;
    os.remove(configs.DAY_GOALS_DB_PATH+datafile_name+'.json')
