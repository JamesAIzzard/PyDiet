from typing import  TYPE_CHECKING
import json
import uuid
import pydiet.configs as configs
from pydiet.configs import INGREDIENT_DB_PATH
if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient

class RepoService():
    def __init__(self):
        pass

    @staticmethod
    def create_ingredient(ingredient:'Ingredient')->None:
        '''Saves the ingredient to the database.
        '''
        filename = str(uuid.uuid4())+'.json'
        with open(configs.INGREDIENT_DB_PATH+filename, 'w') as fh:
            json.dump(ingredient._data, fh, indent=2)