import json
from pathlib import Path
from pydiet.ingredients.ingredient import Ingredient

_cwd = str(Path.cwd())

INGREDIENT_DATAFILE_TEMPLATE_PATH = _cwd+'/pydiet/database/ingredients/template.json'
MANDATORY_NUTRIENTS = [
    'total_carbohydrate',
    'total_fat',
    'saturated_fat',
    'sugars',
    'fibre',
    'protein',
    'sodium'
]

current_data:dict = {}
current_ingredient = {}

def get_data_template() -> dict:
    '''Returns an ingredient data dictionary object.
    
    Returns:
        dict: A dictionary, containing the ingredient data.
    '''
    # Read the template contents;
    with open(INGREDIENT_DATAFILE_TEMPLATE_PATH) as fh:
        template_data = fh.read()
        # Parse into dict;
        template_dict = json.loads(template_data)
        return template_dict

def summarise(data:dict) -> str:
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