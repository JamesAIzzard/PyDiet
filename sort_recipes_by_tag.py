"""Writes a .json file to collect recipes by tag."""
import json


import model
import persistence

# Configure the target database;
use_test_db = False

if use_test_db:
    persistence.configs.PATH_INTO_DB = 'C:/Users/james.izzard/Dropbox/pydiet/tests/test_database'

recipe_index = persistence.read_index(model.recipes.RecipeBase)

num_recs = len(recipe_index)

data = {}
i = 0
for recipe_dfn in recipe_index:
    i += 1
    r = model.recipes.SettableRecipe(persistence.load_datafile(cls=model.recipes.RecipeBase, datafile_name=recipe_dfn))

    for tag in r.tags:
        if tag not in data:
            data[tag] = []
        data[tag].append(r.datafile_name)

    print(f'{round((i/num_recs)*100, 2)}% Completed...')

with open(f'{persistence.configs.PATH_INTO_DB}/precalc_data/recipes_by_tag.json', 'w') as fh:
    json.dump(data, fh, indent=2, sort_keys=True)

print("Done.")
