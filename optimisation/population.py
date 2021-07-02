"""Population class, used for collecting and managing solutions."""
import logging
import random
from typing import Optional, List, Callable

import model
import optimisation
from optimisation import configs


class Population:
    """Models a population of solutions."""

    def __init__(
            self,
            create_random_member: Callable[[], 'model.meals.SettableMeal'],
            calculate_fitness: Callable[['model.meals.SettableMeal'], List[float]],
            on_population_size_change: Optional[Callable[[int], None]] = None,
            max_size: int = configs.ga_configs["max_population_size"],
            log_fittest_member: Optional[Callable[[int, 'model.meals.MealData'], None]] = None
    ):
        self._log_fittest_member = log_fittest_member
        self._calculate_fitness = calculate_fitness
        self._max_size = max_size
        self._create_random_member = create_random_member
        self._on_population_size_change = on_population_size_change

        self._population = []
        self._highest_fitness_score: Optional[float] = None
        self._fittest_member: Optional['model.meals.SettableMeal'] = None
        self._generation: int = 1

    def __len__(self):
        return len(self._population)

    def populate_with_random_members(self):
        """Increases the population size to maximum by generating random members."""
        while len(self._population) < self._max_size:
            self.append(self._create_random_member())

    def choose_two_random_members(self):
        """Selects two members from the population at random."""
        m1 = random.choice(self._population)
        m2 = random.choice(self._population)
        # Prevent the same member being returned twice;
        while m1 is m2:
            m2 = random.choice(self._population)

        return m1, m2

    @property
    def generation(self) -> int:
        """Returns the current population generation."""
        return self._generation

    def inc_generation(self):
        """Increments the generation counter."""
        self._generation += 1

    @property
    def highest_fitness_score(self) -> float:
        """Returns the highest fitness score."""
        return self._highest_fitness_score

    @property
    def fittest_member(self) -> 'model.meals.SettableMeal':
        """Returns the fittest member in the population."""
        return self._fittest_member

    def _update_fittest_member(self, fitness, member):
        """Updates the record of the fittest member in the population."""
        self._highest_fitness_score, self._fittest_member = fitness, member
        if self._log_fittest_member is not None:
            self._log_fittest_member(self._generation, member.persistable_data)

    def append(self, member: 'model.meals.SettableMeal'):
        """Adds member to population."""
        # Prevent a member being added twice;
        if member in self._population:
            raise ValueError("Member cannot be added to population twice.")
        # Calculate the fitness of the new member;
        fitness = optimisation.calculate_fitness(member)[0]
        # If this is the first member, or beats the current best member, update the fittest member;
        if len(self._population) == 0 or fitness > self.highest_fitness_score:
            logging.info(f"-> New best solution: {fitness} <-")
            self._update_fittest_member(fitness, member)
        # Add it to the population;
        self._population.append(member)
        # Trigger the on_size_change;
        if self._on_population_size_change is not None:
            self._on_population_size_change(len(self._population))

    def remove(self, member: 'model.meals.SettableMeal') -> None:
        self._population.remove(member)
        # Trigger the on_size_change;
        if self._on_population_size_change is not None:
            self._on_population_size_change(len(self._population))
