"""Script to create a recipe datafile."""
from unittest import mock

import model
import persistence
import tests

# Configure the target database;
# target_db = "real"
target_db = "test"

# Create new recipe instance;
sr = model.recipes.SettableRecipe()

# Set the parameters;
sr.name = "Banana Milkshake"
sr.add_ingredient_quantity("Banana", 150, 'g')
sr.add_ingredient_quantity("Milk (Skimmed)", 1, 'pint')
sr.add_ingredient_quantity("Honey", 25, 'g')
sr.add_serve_interval("04:00-10:00")
sr.add_serve_interval("12:00-13:00")
sr.add_serve_interval("16:00-18:00")
sr.instruction_src = "https://www.bbcgoodfood.com/recipes/banana-milkshake"
sr.add_tags(["drink", "sweet"])

if target_db == "test":
    with mock.patch('persistence.configs.path_into_db', tests.persistence.configs.path_into_db):
        persistence.save_instance(sr)
else:
    persistence.save_instance(sr)
