from typing import Union, Dict, Callable, TypedDict, TYPE_CHECKING
import json
import uuid

from pydiet import repository

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import IngredientData

def _create_indexed_datafile(data: Union[Dict, TypedDict],
                             path_to_db_dir: str,
                             read_index_func: Callable,
                             update_index_func: Callable) -> str:
    '''Writes a data dictionary to a new datafile on the disk.

    Args:
        data (Dict): The data dictionary to write.
        read_index_func (Callable): Function to return the relevant index as a dict.
        update_index_func (Callable): Function to update the relevant index on disk.

    Returns:
        str: The datafile's filename on disk.
    '''
    # Check the 'name' field in the datafile is populated;
    if not data['name']:
        raise ValueError('The name field is not populated.')
    # Check the 'name' field in the datafile is unique;
    index = read_index_func()
    if data['name'] in index.values():
        raise ValueError('The name field is not unique')

    # Create the unique filename;
    filename = str(uuid.uuid4())
    filename_w_ext = filename+'.json'
    filepath = path_to_db_dir+filename_w_ext

    # Update the index with the filename;
    index[filename] = data['name']
    update_index_func(index)

    # Write the ingredient datafile;
    with open(filepath, 'w') as fh:
        json.dump(data, fh, indent=2, sort_keys=True)

    # Return the filename;
    return filename


def _read_json_datafile(filepath: str) -> Dict:
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


def _update_index(index: Dict, filepath: str) -> None:
    '''Updates an index with the new data dict provided.

    Args:
        index (Dict): Index data.
        filepath (str): Index filepath.
    '''
    with open('{filepath}'.format(
            filepath=filepath), 'w') as fh:
        json.dump(index, fh, indent=2, sort_keys=True)


def create_ingredient_data(ingredient_data: 'IngredientData') -> str:
    '''Writes an ingredient data dict to a new ingredient
    datafile on disk.

    Args:
        ingredient_data (Dict): Ingredient data dictionary.

    Returns:
        str: The filename for the ingredient datafile on disk.
    '''
    return _create_indexed_datafile(
        ingredient_data, 
        repository.configs.ingredient_db_path,
        read_ingredient_index, 
        update_ingredient_index)


# def create_recipe_data(recipe_data: Dict) -> str:
#     '''Writes an recipe data dict to a new recipe
#     datafile on disk.

#     Args:
#         recipe_data (Dict): Recipe data dictionary.

#     Returns:
#         str: The filename for the recipe datafile on disk.
#     '''
#     return _create_indexed_datafile(recipe_data, read_recipe_index, update_recipe_index)


# def create_day_goals_data(day_goals_data: Dict) -> str:
#     '''Writes an daygoals data dict to a new daygoals
#     datafile on disk.

#     Args:
#         day_goals_data (Dict): DayGoals data dictionary.

#     Returns:
#         str: The filename for the daygoals datafile on disk.
#     '''
#     return _create_indexed_datafile(day_goals_data, read_day_goals_index, update_day_goals_index)


def read_ingredient_data(ingredient_datafile_name: str) -> Dict:
    '''Returns an ingredient datafile as a dict.

    Args:
        ingredient_datafile_name (str): Filename of ingredient
            datafile, without the extension.

    Returns:
        Dict: Ingredient datafile in dictionary format.
    '''
    return _read_json_datafile('{path_to}+{filename}.json'.format(
        path_to=repository.configs.ingredient_db_path,
        filename=ingredient_datafile_name
    ))


# def read_recipe_data(recipe_datafile_name: str) -> Dict:
#     '''Returns an recipe datafile as a dict.

#     Args:
#         recipe_datafile_name (str): Filename of recipe
#             datafile, without the extension.

#     Returns:
#         Dict: recipe datafile in dictionary format.
#     '''
#     return _read_json_datafile('{path_to}+{filename}.json'.format(
#         path_to=repository.configs.RECIPE_DB_PATH,
#         filename=recipe_datafile_name
#     ))


# def read_day_goals_data(day_goals_datafile_name: str) -> Dict:
#     '''Returns an day goals datafile as a dict.

#     Args:
#         day_goals_datafile_name (str): Filename of day goals
#             datafile, without the extension.

#     Returns:
#         Dict: day goals datafile in dictionary format.
#     '''
#     return _read_json_datafile('{path_to}+{filename}.json'.format(
#         path_to=repository.configs.DAY_GOALS_DB_PATH,
#         filename=day_goals_datafile_name
#     ))


# def read_global_day_goals_data() -> Dict:
#     '''Returns the saved global day goals data as a dict.

#     Returns:
#         Dict: Global day goals data.
#     '''
#     return _read_json_datafile(repository.configs.GLOBAL_DAY_GOALS_DB_PATH)


def read_ingredient_index() -> Dict[str, str]:
    '''Returns the saved ingredient index as a dict;

    Returns:
        Dict[str, str]: The saved ingredients index.
    '''
    return _read_json_datafile('{ingredient_db_path}{index_name}.json'.format(
        ingredient_db_path=repository.configs.ingredient_db_path,
        index_name=repository.configs.indexes_filename
    ))


# def read_recipe_index() -> Dict[str, str]:
#     '''Returns the saved recipe index as a dict;

#     Returns:
#         Dict[str, str]: The saved recipe index.
#     '''
#     return _read_json_datafile('{recipe_db_path}{index_name}.json'.format(
#         recipe_db_path=repository.configs.RECIPE_DB_PATH,
#         index_name=repository.configs.RECIPE_INDEX_NAME
#     ))


# def read_day_goals_index() -> Dict[str, str]:
#     '''Returns the saved daygoals index as a dict;

#     Returns:
#         Dict[str, str]: The saved daygoals index.
#     '''
#     return _read_json_datafile('{day_goals_db_path}{index_name}.json'.format(
#         day_goals_db_path=repository.configs.DAY_GOALS_DB_PATH,
#         index_name=repository.configs.DAY_GOALS_INDEX_NAME
#     ))


def _update_indexed_datafile(data: Union[Dict, TypedDict],
                             path_to_db_dir: str,
                             datafile_name: str,
                             read_index_func: Callable,
                             update_index_func: Callable) -> None:
    '''Updates an indexed datafile on disk, with new data.

    Args:
        data (Dict): Data to be written.
        path_to_db_dir (str): Path to the folder containing the datafiles.
        datafile_name (str): Name of the datafile to write to.
        read_index_func (Callable): Function used to read the relevant index file.
        update_index_func (Callable): Function used to update the relevant index file.
    '''
    # Load the index to do some checks;
    index = read_index_func()
    # Check the ingredient name is populated;
    if not data['name']:
        raise ValueError('The name field is not populated.')
    # Check the name is not used by another datafile;
    # Pop the current name, because if it hasn't changed, we don't want to
    # detect it;
    index.pop(datafile_name)
    # Now current has been removed, check everwhere else for name;
    if data['name'] in index.values():
        raise ValueError('The name field is not unique.')

    # Write the data;
    with open('{path_to_db_dir}{datafile_name}.json'.format(
        path_to_db_dir=path_to_db_dir,
        datafile_name=datafile_name
    ), 'w') as fh:
        json.dump(data, fh, indent=2, sort_keys=True)

    # Update the index;
    index[datafile_name] = data['name']
    update_index_func(index)


def update_ingredient_data(ingredient_data: 'IngredientData', datafile_name: str) -> None:
    '''Updates an ingredient datafile with new data.

    Args:
        ingredient_data (Dict): New data.
        datafile_name (str): Name of datafile to write to.
    '''
    _update_indexed_datafile(
        ingredient_data,
        repository.configs.ingredient_db_path,
        datafile_name,
        read_ingredient_index,
        update_ingredient_index)


# def update_recipe_data(recipe_data: Dict, datafile_name: str) -> None:
#     '''Updates a recipe datafile with new data.

#     Args:
#         recipe_data (Dict): New data.
#         datafile_name (str): Name of datafile to write to.
#     '''
#     _update_indexed_datafile(
#         recipe_data,
#         repository.configs.RECIPE_DB_PATH,
#         datafile_name,
#         read_recipe_index,
#         update_recipe_index
#     )


# def update_day_goals_data(day_goals_data: Dict, datafile_name: str) -> None:
#     '''Updates a daygoals datafile with new data.

#     Args:
#         day_goals_data (Dict): New data.
#         datafile_name (str): Name of datafile to write to.
#     '''
#     _update_indexed_datafile(
#         day_goals_data,
#         repository.configs.DAY_GOALS_DB_PATH,
#         datafile_name,
#         read_day_goals_index,
#         update_day_goals_index
#     )


# def update_global_day_goals_data(global_day_goals_data: Dict) -> None:
#     '''Updates the global daygoals data with the new dict supplied.

#     Args:
#         global_day_goals_data (Dict): New global daygoals data dict.
#     '''
#     # Write the data;
#     with open(repository.configs.GLOBAL_DAY_GOALS_DB_PATH, 'w') as fh:
#         json.dump(global_day_goals_data, fh, indent=2, sort_keys=True)


def update_ingredient_index(index: Dict[str, str]) -> None:
    '''Updates the ingredient index with the new datafile provided.

    Args:
        index (Dict[str, str]): New index data.
    '''
    _update_index(index, '{db_path}{index_name}.json'.format(
        db_path=repository.configs.ingredient_db_path,
        index_name=repository.configs.indexes_filename
    ))


# def update_recipe_index(index: Dict[str, str]) -> None:
#     '''Updates the recipe index with the new datafile provided.

#     Args:
#         index (Dict[str, str]): New index data.
#     '''
#     _update_index(index, '{db_path}{index_name}.json'.format(
#         db_path=repository.configs.RECIPE_DB_PATH,
#         index_name=repository.configs.RECIPE_INDEX_NAME
#     ))


# def update_day_goals_index(index: Dict[str, str]) -> None:
#     '''Updates the daygoals index with the new datafile provided.

#     Args:
#         index (Dict[str, str]): New index data.
#     '''
#     _update_index(index, '{db_path}{index_name}.json'.format(
#         db_path=repository.configs.DAY_GOALS_DB_PATH,
#         index_name=repository.configs.DAY_GOALS_INDEX_NAME
#     ))


# def _delete_indexed_datafile(datafile_path: str,
#                              read_index_func: Callable,
#                              update_index_func: Callable) -> None:
#     '''Deletes an indexed datafile from disk, updating index to reflect deletion.

#     Args:
#         datafile_path (str): Path to datafile for deletion.
#         read_index_func (Callable): Function to read the relevant index.
#         update_index_func (Callable): Function to update the relevant index.
#     '''
#     # Open the index;
#     index = read_index_func()
#     # Remove the entry from the index;
#     index.pop(datafile_path)
#     # Rewrite the index;
#     update_index_func(index)
#     # Delete the datafile;
#     os.remove('{df_path}.json'.format(
#         df_path=datafile_path
#     ))


# def delete_ingredient_data(datafile_name: str) -> None:
#     '''Deletes an ingredient datafile and updates the index.

#     Args:
#         datafile_name (str): Name of datafile to delete.
#     '''
#     _delete_indexed_datafile('{db_path}{df_name}.json'.format(
#         db_path=repository.configs.INGREDIENT_DB_PATH,
#         df_name=datafile_name,
#     ), read_ingredient_index, update_ingredient_index)


# def delete_recipe_data(datafile_name: str) -> None:
#     '''Deletes an recipe datafile and updates the index.

#     Args:
#         datafile_name (str): Name of datafile to delete.
#     '''
#     _delete_indexed_datafile('{db_path}{df_name}.json'.format(
#         db_path=repository.configs.RECIPE_DB_PATH,
#         df_name=datafile_name,
#     ), read_recipe_index, update_recipe_index)


# def delete_day_goals_data(datafile_name: str) -> None:
#     '''Deletes an ingredient datafile and updates the index.

#     Args:
#         datafile_name (str): Name of datafile to delete.
#     '''
#     _delete_indexed_datafile('{db_path}{df_name}.json'.format(
#         db_path=repository.configs.DAY_GOALS_DB_PATH,
#         df_name=datafile_name,
#     ), read_day_goals_index, update_day_goals_index)
