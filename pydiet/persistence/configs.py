from pathlib import Path

def cwd() -> str:
    return str(Path.cwd())

indexes_filename = 'index'
ingredient_db_path = cwd()+'/pydiet/database/ingredients/'
recipe_db_path = cwd()+'/pydiet/database/recipes/'
day_goals_db_path = cwd()+'/pydiet/database/goals/day_goals/'
global_day_goals_db_path = cwd()+'/pydiet/database/goals/global_day_goals.json'