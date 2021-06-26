"""Top level functionality for optimisation module."""
import random
from typing import List, Dict, Callable, Any

import model
import persistence


def init_population(num_members: int, create_member: Callable) -> List:
    """Returns a randomly generated population of specified size."""
    pop = []
    while len(pop) < num_members:
        pop.append(create_member())
    return pop


def create_random_member(tags: List[str], flags: Dict[str, bool]) -> Any:
    """Creates a random member of the population, with specified tags and flags."""
    meal = model.meals.SettableMeal()
    for tag in tags:
        df_name = random.choice(persistence.get_recipe_df_names_by_tag(tag))
        r_unique_name = model.recipes.get_unique_name_for_datafile_name(df_name)
        typical_serving_size = persistence.get_precalc_data_for_recipe(df_name)['typical_serving_size_g']
        meal.add_recipe(recipe_unique_name=r_unique_name, recipe_qty_data=model.quantity.QuantityData(
            quantity_in_g=typical_serving_size,
            pref_unit='g'
        ))
    return meal
