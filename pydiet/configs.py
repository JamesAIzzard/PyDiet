from pathlib import Path

def cwd()->str:
    return str(Path.cwd())

INGREDIENT_DATAFILE_TEMPLATE_PATH = cwd()+'/pydiet/database/ingredients/template.json'
MANDATORY_NUTRIENTS = [
    'total_carbohydrate',
    'total_fat',
    'saturated_fat',
    'sugars',
    'fibre',
    'protein',
    'sodium'
]

INGREDIENT_DB_PATH = cwd()+'/pydiet/database/ingredients/'