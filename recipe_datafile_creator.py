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
sr.name = "Porridge"
sr.add_ingredient_quantity("Oats (Whole)", 60, 'g')
sr.add_ingredient_quantity("Sultana", 15, 'g')
sr.add_ingredient_quantity("Milk (Skimmed)", 100, 'ml')
sr.add_serve_interval("04:00-10:00")
sr.instruction_src = "https://www.bbcgoodfood.com/recipes/perfect-porridge"
sr.add_tags(["main"])

if target_db == "test":
    with mock.patch('persistence.configs.path_into_db', tests.persistence.configs.path_into_db):
        persistence.save_instance(sr)
else:
    persistence.save_instance(sr)
