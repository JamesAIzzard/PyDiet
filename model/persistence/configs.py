from pathlib import Path


def cwd() -> str:
    return str(Path.cwd())


path_into_db = 'c:/users/james.izzard/dropbox/pydiet/database/'
ingredient_db_path = path_into_db + 'ingredients/'
recipe_db_path = path_into_db + 'recipes/'
meal_goals_db_path = path_into_db + 'goals/meal_goals/'
day_goals_db_path = path_into_db + 'goals/day_goals/'
global_day_goals_db_path = path_into_db + 'goals/global_day_goals.json'
