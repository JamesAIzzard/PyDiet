import json
from pathlib import Path

_cwd = str(Path.cwd())

INGREDIENT_DATAFILE_TEMPLATE_PATH = _cwd+'/pydiet/database/ingredients/template.json'

current_ingredient_datafile = None

def get_ingredient_data_template():
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