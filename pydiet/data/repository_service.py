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

def create_ingredient_data(ingredient_data:Dict)->str:
    # Check the ingredient name does not exist already;
    index = read_ingredient_index()
    if ingredient_data['name'] in index.values():
        raise DuplicateIngredientNameError('There is already an ingredient called {}'.format(ingredient_data['name']))
    # Create filename;
    filename = str(uuid.uuid4())
    filename_w_ext = filename+'.json'    
    # Update index with filename;
    index[filename] = ingredient_data['name']
    update_ingredient_index(index)
    # Write the ingredient datafile;
    with open(configs.INGREDIENT_DB_PATH+filename_w_ext, 'w') as fh:
        json.dump(ingredient_data, fh, indent=2, sort_keys=True)    
    # Return the datafile name;
    return filename

def read_ingredient_template_data() -> Dict:
    return read_ingredient_data(
        configs.INGREDIENT_DATAFILE_TEMPLATE_NAME)


def read_ingredient_data(ingredient_datafile_name: str) -> Dict:
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

def update_ingredient_data(ingredient_data:Dict, datafile_name:str) -> None:
    # Check the ingredient name is not also used somwhere else;
    index = read_ingredient_index()
    ## Pop the current name, because if it hasn't changed, we don't want to
    ## detect it;
    index.pop(datafile_name)
    ## Now current has been removed, check everwhere else for name;
    if ingredient_data['name'] in index.values():
        raise DuplicateIngredientNameError('Another ingredient already uses the name {}'.format(ingredient_data['name']))
    # Write the ingredient data;
    with open(configs.INGREDIENT_DB_PATH+datafile_name+'.json', 'w') as fh:
        json.dump(ingredient_data, fh, indent=2, sort_keys=True)    
    # Update the index;
    index[datafile_name] = ingredient_data['name']
    update_ingredient_index(index)

def update_ingredient_index(index: Dict[str, str]) -> None:
    with open(configs.INGREDIENT_DB_PATH+'{}.json'.
              format(configs.INGREDIENT_INDEX_NAME), 'r+') as fh:
        json.dump(index, fh, indent=2, sort_keys=True)

