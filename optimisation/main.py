"""Top level functionality for optimisation module."""
import logging
import random
from typing import List, Dict, Callable, Optional

import numpy
from matplotlib import pylab

import model
import persistence
from optimisation import configs


class Plotter:
    def __init__(self):
        self.


class Population:

    def __init__(self):
        self._population = []
        self.highest_fitness_score: Optional[float] = None
        self.highest_fitness_member: Optional['model.meals.SettableMeal'] = None
        self.fitness_hist = []

    def __str__(self):
        return f"{self._population}"

    def __len__(self):
        return len(self._population)

    def __getitem__(self, i):
        return self._population.__getitem__(i)

    def __iter__(self):
        return self._population.__iter__()

    def append(self, member: 'model.meals.SettableMeal'):
        """Adds member to population."""
        if member in self._population:
            raise ValueError("Member cannot be added to population twice.")
        fitness = calculate_fitness(member)
        if self.highest_fitness_score is None:
            self.highest_fitness_score = fitness
            self.highest_fitness_member = member
        elif fitness > self.highest_fitness_score:
            self.fitness_hist.append(self.highest_fitness_score)
            self.highest_fitness_score = fitness
            self.highest_fitness_member = member
        self._population.append(member)

    def remove(self, member: 'model.meals.SettableMeal') -> None:
        self._population.remove(member)


def run(ga_configs=configs.ga_configs, constraints=configs.constraints):
    """Runs the GA."""

    logging.info("--- Optimisation Run Starting ---")
    logging.info("Beginning population growth.")
    plot = Plotter()
    pop = init_population(
        num_members=ga_configs["max_population_size"],
        create_member=lambda: create_random_member(
            tags=constraints['tags'],
            flags=constraints['flags']
        )
    )
    logging.info("Initial population created.")

    logging.info("Beginning optimisation loop.")
    gen: int = 0

    # Run the main loop
    while gen < ga_configs['max_generations'] and pop.highest_fitness_score < ga_configs['acceptable_fitness']:
        logging.info(f"Generation #{gen}")
        cull_population(pop)
        regrow_population(pop)
        gen += 1
    logging.info("Finished optimisation.")


def cull_population(
        population: 'Population',
        max_population_size: int = configs.ga_configs['max_population_size'],
        cull_percentage: float = configs.ga_configs['cull_percentage']) -> None:
    """Culls the population to the minimum level."""
    culled_pop_size = round(max_population_size * (1 - (cull_percentage / 100)))
    logging.info(f"Culling population to {culled_pop_size} members.")
    while len(population) > culled_pop_size:
        m1 = random.choice(population)
        m2 = random.choice(population)
        while m2 == m1:
            m2 = random.choice(population)
        m1f = calculate_fitness(m1)
        m2f = calculate_fitness(m2)
        if m1f < m2f:
            population.remove(m2)
        else:
            population.remove(m1)
    logging.info("Population culling complete.")


def should_mutate(mutation_prob_perc: float = configs.ga_configs['mutation_probability_percentage']) -> bool:
    """Returns True/False to indicate if the population should mutate."""
    point = random.choice(numpy.linspace(0, 100, num=100))
    if point < mutation_prob_perc:
        return True
    else:
        return False


def regrow_population(
        population: 'Population',
        max_population_size: int = configs.ga_configs['max_population_size'],
        mutation_prob: float = configs.ga_configs['mutation_probability_percentage'],
        random_solution_prob: float = configs.ga_configs['random_solution_intro_percentage']
) -> None:
    """Regrows the population back to correct level."""
    logging.info(f"Regrowing population to {max_population_size} members.")
    perc = 0
    while len(population) < max_population_size:
        if should_mutate(random_solution_prob):
            m = create_random_member()
            logging.debug("Mutation: Solution randomly created.")
        else:
            m = splice_members(random.choice(population), random.choice(population))
            if should_mutate(mutation_prob_perc=mutation_prob):
                mutate_member(m)
                logging.debug("Mutation: Spliced solution mutated.")
        population.append(m)
        if round(len(population) / max_population_size, 1) > perc:
            perc = round(len(population) / max_population_size, 1)
            logging.info(f"{perc * 100}% complete, max_fitness = {population.highest_fitness_score}")
    logging.info(f"Finished regrowing population.")


def init_population(num_members: int, create_member: Callable) -> 'Population':
    """Returns a randomly generated population of specified size."""
    pop = Population()
    perc = 0
    while len(pop) < num_members:
        m = create_member()
        pop.append(m)
        if round(len(pop) / num_members, 1) > perc:
            perc = round(len(pop) / num_members, 1)
            logging.info(f"{perc * 100}% complete, max_fitness = {pop.highest_fitness_score}")
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


def calculate_fitness(
        m: 'model.meals.SettableMeal',
        target_nutr_masses: Dict[str, float] = configs.goals['target_nutrient_masses']
):
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


def create_random_member(
        tags: List[str] = configs.constraints['tags'],
        flags: Dict[str, bool] = configs.constraints['flags']
) -> 'model.meals.SettableMeal':
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
    run()
