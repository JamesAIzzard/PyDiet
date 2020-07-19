from pathlib import Path

def cwd() -> str:
    return str(Path.cwd())

INGREDIENT_DATAFILE_TEMPLATE_NAME = 'template'
RECIPE_DATAFILE_TEMPLATE_NAME = 'template'
INGREDIENT_INDEX_NAME = 'index'
RECIPE_INDEX_NAME = 'index'
DAY_GOALS_INDEX_NAME = 'index'
INGREDIENT_DB_PATH = cwd()+'/pydiet/database/ingredients/'
RECIPE_DB_PATH = cwd()+'/pydiet/database/recipes/'
DAY_GOALS_DB_PATH = cwd()+'/pydiet/database/goals/day_goals/'
GLOBAL_DAY_GOALS_DB_PATH = cwd()+'/pydiet/database/goals/global_day_goals.json'