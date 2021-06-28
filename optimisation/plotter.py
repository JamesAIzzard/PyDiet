"""Graphing functionality to display results from the optimiser."""
from matplotlib import pyplot as plt


class Plotter:
    """Provides result plotting functionality."""

    def __init__(self):
        self.fig = plt.figure(1)
        self.manager = plt.get_current_fig_manager()
        self.manager.set_window_title("PyDiet")
        self.fitness_hist_ax = self.fig.add_subplot(1, 1, 1)
        self.fitness_hist_ax.set_xlabel('Generation #')
        self.fitness_hist_ax.set_ylabel('Fitness Score')
        self.fitness_hist_ax.grid()

        self.fitness_hist = []
        self.generation_hist = []

        plt.ion()

    def update(self):
        self.fitness_hist_ax.clear()
        self.fitness_hist_ax.plot(self.fitness_hist, self.generation_hist)
        plt.show()