"""Population class, used for collecting and managing solutions."""
from typing import Optional, Callable

import model
import optimisation


class Population:
    """Models a population of solutions."""

    def __init__(
            self,
            on_new_best: Optional[Callable[[int, 'model.meals.MealData'], None]] = None
    ):
        self._population = []
        self.highest_fitness_score: Optional[float] = None
        self.highest_fitness_member: Optional['model.meals.SettableMeal'] = None
        self.fitness_hist = []
        self._on_new_best = on_new_best
        self._generation: int = 1

    def __str__(self):
        return f"{self._population}"

    def __len__(self):
        return len(self._population)

    def __getitem__(self, i):
        return self._population.__getitem__(i)

    def __iter__(self):
        return self._population.__iter__()

    def next_generation(self):
        """Increments the generation counter."""
        self._generation += 1

    @property
    def generation(self) -> int:
        """Returns the current population generation."""
        return self._generation

    def append(self, member: 'model.meals.SettableMeal'):
        """Adds member to population."""
        if member in self._population:
            raise ValueError("Member cannot be added to population twice.")
        fitness = optimisation.calculate_fitness(member)
        if self.highest_fitness_score is None:
            self.highest_fitness_score = fitness
            self.highest_fitness_member = member
            self._on_new_best(self._generation, member.persistable_data)
        elif fitness > self.highest_fitness_score:
            self.fitness_hist.append(self.highest_fitness_score)
            self.highest_fitness_score = fitness
            self.highest_fitness_member = member
            self._on_new_best(self._generation, member.persistable_data)
        self._population.append(member)

    def remove(self, member: 'model.meals.SettableMeal') -> None:
        self._population.remove(member)
