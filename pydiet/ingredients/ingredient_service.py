from typing import Dict, TYPE_CHECKING
import json
import pydiet.configs as configs
from pydiet.ingredients.ingredient import Ingredient
if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient

class IngredientService():
    def __init__(self):
        self.current_data:Dict
        self.current_ingredient:'Ingredient'


    def get_data_template(self) -> dict:
        '''Returns an ingredient data dictionary object.
        
        Returns:
            dict: A dictionary, the blank data template.
        '''
        # Read the template contents;
        with open(configs.INGREDIENT_DATAFILE_TEMPLATE_PATH) as fh:
            template_data = fh.read()
            # Parse into dict;
            template_dict = json.loads(template_data)
            return template_dict

    def summarise(self, data:dict) -> str:
        # Configure some default values;
        summary:str = '''Ingredient Summary:
-----------------------------
Name: {name}
Cost for {cost_mass}{cost_mass_units}: £{cost_gbp}
'''.format(
        name=data['name'],
        cost_mass=data['cost_per_mass']['mass'],
        cost_mass_units=data['cost_per_mass']['mass_units']
    )
        return summary

ingredient_service = IngredientService()