import json
import uuid
from pathlib import Path

_cwd = str(Path.cwd())

INGREDIENT_DB_PATH = _cwd+'/pydiet/database/ingredients/'

def create_ingredient(ingredient):
    '''Saves the ingredient to the database.
    '''
    filename = str(uuid.uuid4())+'.json'
    with open(INGREDIENT_DB_PATH+filename, 'w') as fh:
        json.dump(ingredient.data, fh, indent=2)