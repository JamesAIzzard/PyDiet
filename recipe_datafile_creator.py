"""Script to create a recipe datafile."""

import model
import persistence
import tests

# Configure the target database;
use_test_db = True

if use_test_db:
    persistence.configs.PATH_INTO_DB = 'C:/Users/james.izzard/Dropbox/pydiet/tests/test_database'

# Create new recipe instance;
sr = model.recipes.SettableRecipe()

# Set the parameters;
sr.name = "Peanut Butter Toast"
sr.add_ingredient_quantity("Bread (Wholemeal)", 150, 'g')
sr.add_ingredient_quantity("Butter", 20, 'g')
sr.add_ingredient_quantity("Peanut Butter", 40, 'g')
sr.add_serve_interval("12:00-13:00")
sr.add_serve_interval("16:00-18:00")
sr.add_tags(["main"])

# Save the new recipe instance;
persistence.save_instance(sr)
