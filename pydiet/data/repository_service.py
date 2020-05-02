from typing import Dict, TYPE_CHECKING
import json
import uuid
import pydiet.shared.configs as configs
from pydiet.shared.configs import INGREDIENT_DB_PATH
if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient

def read_ingredient_data_template() -> Dict:
    return read_ingredient_data(\
        configs.INGREDIENT_DATAFILE_TEMPLATE_NAME)
    

def read_ingredient_data(ingredient_data_filename:str)->Dict:
    '''Returns an ingredient datafile as a dict.
    
    Args:
        ingredient_datafile_name (str): Filename of ingredient
            datafile, without the extension.
    
    Returns:
        Dict: Ingredient datafile in dictionary format.
    '''
    # Read the datafile contents;
    with open(configs.INGREDIENT_DB_PATH+'{}.json'.format(
        ingredient_data_filename), 'r') as fh:
        raw_data = fh.read()
        # Parse into dict;
        data = json.loads(raw_data)
        # Return it;
        return data

def create_ingredient_data(ingredient_data:Dict)->None:
    '''Saves the ingredient to the database.
    '''
    filename = str(uuid.uuid4())+'.json'
    with open(configs.INGREDIENT_DB_PATH+filename, 'w') as fh:
        json.dump(ingredient_data, fh, indent=2, sort_keys=True)

def update_ingredient_data(
    ingredient_data:Dict, 
    ingredient_data_filename:str
)->None:
    with open(configs.INGREDIENT_DB_PATH+'{}.json'\
        .format(ingredient_data_filename), 'r+') as fh:
        json.dump(ingredient_data, fh, indent=2, sort_keys=True)