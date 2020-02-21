import json

INGREDIENT_DATAFILE_TEMPLATE_PATH = '../database/ingredients/template.json'

def create_new_ingredient_datafile():
    # Read the template contents;
    with open(INGREDIENT_DATAFILE_TEMPLATE_PATH) as fh:
        template_data = fh.read()
        # Parse into dict;
        template_dict = json.loads(template_data)
        return template_dict