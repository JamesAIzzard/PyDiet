"""Script to populate the recipe database with random recipes."""
import random
from RandomWordGenerator import RandomWord

import model
import persistence

NUM_RECIPES = 10000
MAX_INGREDIENTS = 10
MIN_INGREDIENTS = 2
MAX_INGREDIENT_QTY_G = 500
MIN_INGREDIENT_QTY_G = 10
SERVE_INTERVALS = [
    "01:00-06:00",
    "06:00-10:00",
    "10:00-14:00",
    "14:00-16:00",
    "16:00-20:00",
    "20:00-23:00"
]

# Init the random word generator;
rw = RandomWord(max_word_size=10)

# Load the ingredient index;
iindex = persistence.read_index(cls=model.ingredients.IngredientBase)

# List to compile the recipes;
recipes = []

# While we haven't yet generated the required number of recipes;
for i in range(0, NUM_RECIPES):
    # Create the recipe instance;
    r = model.recipes.SettableRecipe()

    # Name the recipe;
    r.name = rw.generate().lower()

    # Randomly populate ingredients;
    # First choose a number of ingredients;
    i_count = random.choice(range(MIN_INGREDIENTS, MAX_INGREDIENTS))
    # Now add a random ingredient for each number;
    for iqn in range(0, i_count):
        # Choose an ingredient at random;
        idf_name = random.choice(list(iindex.values()))
        r.add_ingredient_quantity(
            ingredient_unique_name=idf_name,
            qty_value=random.randrange(
                start=MIN_INGREDIENT_QTY_G,
                stop=MAX_INGREDIENT_QTY_G
            ),
            qty_unit='g'
        )

    # Now choose a serve interval;
    r.add_serve_interval(random.choice(SERVE_INTERVALS))

    # Now choose a tag;
    r.add_tags([random.choice(model.tags.configs.ALL_TAGS)])

    # Add the recipe to the list;
    recipes.append(r)
    print(i)

    # Save the recipe;
    persistence.save_instance(r)