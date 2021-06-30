"""Graphing functionality to display results from the optimiser."""
import json
import threading
from matplotlib import pyplot as plt
from matplotlib import animation

import model
import optimisation


class Plotter:
    """Provides result plotting functionality."""

    def __init__(self):
        self.fig = plt.figure(1)
        self.fig.canvas.manager.set_window_title("PyDiet")
        self.fitness_hist_ax = self.fig.add_subplot(1, 1, 1)
        self.fitness_hist_ax.set_xlabel('Generation #')
        self.fitness_hist_ax.set_ylabel('Fitness Score')
        self.fitness_hist_ax.grid()
        self._ani = None

    def _update(self):
        """Update function."""
        gens = []
        fitnesses = []
        with open("history.json", 'r') as fh:
            raw_data = fh.read()
            data = json.loads(raw_data)
        for row in data:
            gens.append(row[0])
            m = model.meals.SettableMeal(meal_data=row[1])
            fitnesses.append(optimisation.calculate_fitness(m))
        self.fitness_hist_ax.plot(gens, fitnesses)

    def start(self):
        """Starts plotting results."""
        self._ani = animation.FuncAnimation(self.fig, self._update, interval=500)
        th = threading.Thread(target=lambda: plt.show())
