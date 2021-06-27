"""Top level functionality for optimisation module."""
import logging
import random
from typing import List, Dict, Callable

import numpy

import model
import optimisation
import persistence


def run(configs, constraints, goals):
    """Runs the GA."""
    logging.info("--- Optimisation Run Starting ---")
    logging.info("Beginning population growth.")
    pop = init_population(
        num_members=configs["max_population_size"],
        create_member=lambda: create_random_member(
            tags=constraints['tags'],
            flags=constraints['flags']
        )
    )
    logging.info("Initial population created.")


def init_population(num_members: int, create_member: Callable) -> List:
    """Returns a randomly generated population of specified size."""
    pop = []
    perc = 0
    while len(pop) < num_members:
        m = create_member()
        pop.append(m)
        if round(len(pop) / num_members, 1) > perc:
            perc = round(len(pop) / num_members, 1)
            logging.info(f"{perc * 100}% complete.")
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


def calculate_fitness(m: 'model.meals.SettableMeal', target_nutr_masses: Dict[str, float]):
    return fitness_function(
        get_nutrient_ratio=lambda nutr_name: m.get_nutrient_ratio(nutr_name).subject_g_per_host_g,
        target_nutrient_masses=target_nutr_masses
    )


def mutate_member(member: 'model.meals.SettableMeal') -> None:
    """Mutates the SettableMeal instance provided."""
    # Choose a recipe on the meal at random;
    r = random.choice(list(member.recipes.values()))

    # Define the max and min values for its qty;
    typical_serving_size_g = r.typical_serving_size_g
    max_qty = typical_serving_size_g * 1.5
    min_qty = typical_serving_size_g / 2

    # Choose a quantity within this range;
    new_qty = random.choice(numpy.linspace(min_qty, max_qty, num=1000))

    # Set the recipe to this new quantity;
    member.set_recipe_quantity(r.name, new_qty, 'g')


def splice_members(member_1: 'model.meals.SettableMeal',
                   member_2: 'model.meals.SettableMeal') -> 'model.meals.SettableMeal':
    """Combines two members to form a hybrid, child member."""
    # Pair off the recipes from each member by tag;
    recipes_by_tag = {}
    rqts = list(list(member_1.recipe_quantities.values()) + list(member_2.recipe_quantities.values()))
    for rqty in rqts:
        if rqty.recipe.tags[0] not in recipes_by_tag:
            recipes_by_tag[rqty.recipe.tags[0]] = []
        recipes_by_tag[rqty.recipe.tags[0]].append(rqty)

    # Create a new meal;
    m = model.meals.SettableMeal()

    # Work through the recipes by tag, and add randomly from parents.
    for tag, rqt_options in recipes_by_tag.items():
        chosen_rqt: 'model.recipes.ReadonlyRecipeQuantity' = random.choice(rqt_options)
        m.add_recipe(recipe_unique_name=chosen_rqt.recipe.name, recipe_qty_data=chosen_rqt.persistable_data)

    # Return spliced child;
    return m


def create_random_member(tags: List[str], flags: Dict[str, bool]) -> 'model.meals.SettableMeal':
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


if __name__ == "__main__":
    logging.basicConfig(
        # filename="log.txt",
        level=logging.INFO,
        format='%(asctime)s: %(message)s',
        filemode="w"
    )
    run(
        configs=optimisation.configs.ga_configs,
        constraints=optimisation.configs.constraints,
        goals=optimisation.configs.goals
    )
