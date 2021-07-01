"""Graphing functionality to display results from the optimiser."""
import json
from matplotlib import pyplot as plt
from matplotlib import animation

import model
import optimisation
from optimisation import configs


class Plotter:
    """Provides result plotting functionality."""

    def __init__(self):
        self.fig = plt.figure(1)
        self.fig.canvas.manager.set_window_title("PyDiet")
        self.fitness_hist_ax = self.fig.add_subplot(1, 1, 1)
        self.fitness_hist_ax.set_xlabel('Generation #')
        self.fitness_hist_ax.set_ylabel('Fitness Score')
        self.fitness_hist_ax.grid()
        self.fitness_hist_line, = self.fitness_hist_ax.plot([0], [0])
        self._ani = animation.FuncAnimation(self.fig, self.run, interval=500, repeat=True)

    def run(self, i):
        """Update function."""
        gens = [0]
        fitnesses = [0]
        with open(configs.history_path, 'r') as fh:
            raw_data = fh.read()
            data = json.loads(raw_data)
        for row in data:
            gens.append(row[0])
            m = model.meals.SettableMeal(meal_data=row[1])
            fitnesses.append(optimisation.calculate_fitness(m)[0])
        self.fitness_hist_line.set_data(gens, fitnesses)
        self.fitness_hist_ax.relim()
        self.fitness_hist_ax.autoscale_view()

plotter = Plotter()
plt.show()