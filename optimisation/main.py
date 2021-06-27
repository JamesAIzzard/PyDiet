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


def fitness_function(
        get_nutrient_ratio: Callable[[str], float],
        target_nutrient_masses: Dict[str, float]
) -> float:
    """Returns the fitness of the member provided."""

    # Calculate the total mass of the nutrient targets;
    target_nutr_total_mass = sum(target_nutrient_masses.values())

    # Calculate the ideal ratios between the target nutrient masses;
    target_nutrient_ratios = {}
    for nutr_name, target_mass in target_nutrient_masses.items():
        target_nutrient_ratios[nutr_name] = target_mass / target_nutr_total_mass

    # Calculate a fitness component for each target nutrient ratio;
    components = []
    for nutr_name, target_mass in target_nutrient_masses.items():
        components.append(
            abs(get_nutrient_ratio(nutr_name) - target_nutrient_ratios[
                nutr_name]) / len(target_nutrient_ratios))

    # Combine the fitness components;
    fitness = 1 - sum(components)

    # Return the result;
    return fitness


def create_random_member(tags: List[str], flags: Dict[str, bool]) -> Any:
    """Creates a random member of the population, with specified tags and flags."""
    meal = model.meals.SettableMeal()
    for tag in tags:
        recipe_sets = [set(persistence.get_recipe_df_names_by_tag(tag))]
        for flag, value in flags.items():
            recipe_sets.append(set(persistence.get_recipe_df_names_by_flag(flag, value)))
        possible_df_names = set.intersection(*recipe_sets)
        df_name = random.choice(list(possible_df_names))
        r_unique_name = model.recipes.get_unique_name_for_datafile_name(df_name)
        typical_serving_size = persistence.get_precalc_data_for_recipe(df_name)['typical_serving_size_g']
        meal.add_recipe(recipe_unique_name=r_unique_name, recipe_qty_data=model.quantity.QuantityData(
            quantity_in_g=typical_serving_size,
            pref_unit='g'
        ))
    return meal
