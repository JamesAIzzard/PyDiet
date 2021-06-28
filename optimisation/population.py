"""Population class, used for collecting and managing solutions."""
from typing import Optional

import model
import optimisation


class Population:
    """Models a population of solutions."""

    def __init__(self):
        self._population = []
        self.highest_fitness_score: Optional[float] = None
        self.highest_fitness_member: Optional['model.meals.SettableMeal'] = None
        self.fitness_hist = []
        self.generation = 0

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
        fitness = optimisation.calculate_fitness(member)
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
