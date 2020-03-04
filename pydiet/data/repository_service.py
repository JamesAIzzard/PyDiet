import json
import uuid
import pydiet.configs as configs
from pydiet.configs import INGREDIENT_DB_PATH

class RepoService():
    def __init__(self):
        pass

    @staticmethod
    def create_ingredient(ingredient):
        '''Saves the ingredient to the database.
        '''
        filename = str(uuid.uuid4())+'.json'
        with open(configs.INGREDIENT_DB_PATH+filename, 'w') as fh:
            json.dump(ingredient.data, fh, indent=2)

repo_service = RepoService()