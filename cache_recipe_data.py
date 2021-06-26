"""Script to cache recipe data."""
import json


import model
import persistence

# Configure the target database;
use_test_db = True

if use_test_db:
    persistence.configs.PATH_INTO_DB = 'C:/Users/james.izzard/Dropbox/pydiet/tests/test_database'

recipe_index = persistence.read_index(model.recipes.RecipeBase)

num_recs = len(recipe_index)

recipes = {}
i = 0
for recipe_dfn in recipe_index:
    i += 1
    r = model.recipes.SettableRecipe(persistence.load_datafile(cls=model.recipes.RecipeBase, datafile_name=recipe_dfn))

    data = {}
    data['nutrient_ratios_data'] = r.nutrient_ratios_data
    data['ingredient_unique_names'] = r.ingredient_unique_names
    data['ingredient_ratios_data'] = r.ingredient_ratios_data
    data['ingredient_quantities_data'] = r.ingredient_quantities_data
    data['typical_serving_size_g'] = r.typical_serving_size_g
    data['cost_per_qty_data'] = r.cost_per_qty_data
    data['flag_data'] = {}
    for flag_name in model.flags.ALL_FLAGS.keys():
        try:
            data['flag_data'][flag_name] = r.get_flag_value(flag_name)
        except model.flags.exceptions.UndefinedFlagError:
            data['flag_data'][flag_name] = None
    data['calories_per_g'] = r.calories_per_g

    recipes[recipe_dfn] = data

    print(f'{round((i/num_recs)*100, 2)}% Completed...')

if use_test_db:
    cache_path = "tests/test_database/precalc_data"
else:
    cache_path = "cache_ciles"

with open(f'{cache_path}/recipe_cache.json', 'w') as fh:
    json.dump(recipes, fh, indent=2, sort_keys=True)

print("Done.")
