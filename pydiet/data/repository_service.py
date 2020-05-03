from pydiet import data
from typing import Dict, TYPE_CHECKING
import json
import uuid

from pinjector import inject

import pydiet.shared.configs as configs
from pydiet.shared.configs import INGREDIENT_DB_PATH
from pydiet.ingredients.exceptions import DuplicateIngredientNameError
from pydiet.ingredients.ingredient import Ingredient

if TYPE_CHECKING:
    from pydiet.ingredients import ingredient_service


def read_ingredient_data_template() -> Dict:
    return _read_ingredient_data(
        configs.INGREDIENT_DATAFILE_TEMPLATE_NAME)


def _read_ingredient_data(ingredient_datafile_name: str) -> Dict:
    '''Returns an ingredient datafile as a dict.

    Args:
        ingredient_datafile_name (str): Filename of ingredient
            datafile, without the extension.

    Returns:
        Dict: Ingredient datafile in dictionary format.
    '''
    # Read the datafile contents;
    with open(configs.INGREDIENT_DB_PATH+'{}.json'.format(
            ingredient_datafile_name), 'r') as fh:
        raw_data = fh.read()
        # Parse into dict;
        data = json.loads(raw_data)
        # Return it;
        return data


def read_ingredient_index() -> Dict[str, str]:
    with open(configs.INGREDIENT_DB_PATH+'{}.json'.
              format(configs.INGREDIENT_INDEX_NAME)) as fh:
        raw_data = fh.read()
        data = json.loads(raw_data)
        return data

def read_ingredient(datafile_name:str) -> 'Ingredient':
    i_data = _read_ingredient_data(datafile_name)
    return Ingredient(i_data)

def create_ingredient(ingredient: 'Ingredient') -> str:
    igs: 'ingredient_service' = inject('pydiet.ingredient_service')
    # Check that an ingredient with this name does not exist already;
    index = read_ingredient_index()
    if igs.name_already_used(ingredient.name):
        raise DuplicateIngredientNameError()
    # Create a filename for this ingredient;
    filename = str(uuid.uuid4())
    filename_w_ext = filename+'.json'
    # Add filename to index;
    index[filename] = ingredient.name
    # Write the new ingredient;
    with open(configs.INGREDIENT_DB_PATH+filename_w_ext, 'w') as fh:
        json.dump(ingredient._data, fh, indent=2, sort_keys=True)
    # Write the updated datafile;
    _update_ingredient_index(index)
    # Return the filename
    return filename

def resolve_ingredient_datafile_name(ingredient_name:str)->str:
    # Load the ingredient index;
    index = read_ingredient_index()
    for datafile_name in index.keys():
        if index[datafile_name] == ingredient_name:
            return datafile_name
    raise KeyError('Ingredient name was not found.')

def _update_ingredient_index(index: Dict[str, str]) -> None:
    with open(configs.INGREDIENT_DB_PATH+'{}.json'.
              format(configs.INGREDIENT_INDEX_NAME), 'r+') as fh:
        json.dump(index, fh, indent=2, sort_keys=True)


def update_ingredient(ingredient: 'Ingredient', datafile_name: str) -> None:
    # Read the index;
    index = read_ingredient_index()
    # Remove the current line;
    index.pop(datafile_name)
    # Check there are no instances of the name anywhere else;
    if ingredient.name in index.values():
        raise DuplicateIngredientNameError()
    # Write the ingredient data to the datafile;
    with open(configs.INGREDIENT_DB_PATH+datafile_name+'.json', 'w') as fh:
        json.dump(ingredient._data, fh, indent=2, sort_keys=True)
    # Update the ingredient name in the index, in case changed;
    index[datafile_name] = ingredient.name
    _update_ingredient_index(index)
