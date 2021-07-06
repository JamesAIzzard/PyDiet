"""Graphing functionality to display results from the optimiser."""
import json
import random
from typing import Dict, List

from matplotlib import animation
from matplotlib import pyplot as plt

import model
import optimisation
from optimisation import configs


class Plotter:
    """Provides result plotting functionality."""

    def __init__(self, target_nutrient_ratios: Dict[str, float] = configs.goals['target_nutrient_ratios']):
        # Configure the plot;
        self.fig = plt.figure(1)
        self.fig.canvas.manager.set_window_title("PyDiet")
        self.fitness_hist_ax = self.fig.add_subplot(1, 1, 1)
        self.target_ratio_ax = self.fitness_hist_ax.twinx()
        self.target_ratio_ax.set_ylim((0, 1))
        self.target_ratio_ax.set_ylabel('Target Nutrient Ratios')
        self.fitness_hist_ax.set_xlabel('Generation #')
        self.fitness_hist_ax.set_ylabel('Fitness Score')
        self.fitness_hist_ax.grid()
        # Create the lines;
        self.fitness_hist_line, = self.fitness_hist_ax.plot(
            [], [],
            linestyle="--",
            marker="o",
            markersize=4,
            color="b",
            label="Fitness Hist"
        )
        self.target_nutr_lines = {}
        for nutr_name in target_nutrient_ratios.keys():
            _ = self.target_ratio_ax.axhline(
                y=target_nutrient_ratios[nutr_name],
                linestyle='--',
                color="black",
                linewidth=2
            )
            self.target_nutr_lines[nutr_name] = self.target_ratio_ax.plot(
                [], [],
                label=nutr_name
            )
        fh_lines, fh_labels = self.fitness_hist_ax.get_legend_handles_labels()
        tn_lines, tn_labels = self.target_ratio_ax.get_legend_handles_labels()
        lines = fh_lines + tn_lines
        labels = fh_labels + tn_labels
        plt.legend(lines, labels, loc=2)
        self._ani = animation.FuncAnimation(self.fig, self.run, interval=500, repeat=True)

    def run(self, _):
        """Update function."""
        gens = []
        fitnesses = []
        target_nutrs = {nut_name: [] for nut_name in self.target_nutr_lines.keys()}
        with open(configs.history_path, 'r') as fh:
            raw_data = fh.read()
            data = json.loads(raw_data)
        for row in data:
            gens.append(row[0])
            # Strip the nutrient ratios out;
            del row[1]['nutrient_ratios']
            m = model.meals.SettableMeal(meal_data=row[1])
            fitnesses.append(optimisation.calculate_fitness(m)[0])
            for nut_name in self.target_nutr_lines.keys():
                target_nutrs[nut_name].append(m.get_nutrient_ratio(nut_name).subject_g_per_host_g)
        self.fitness_hist_line.set_data(gens, fitnesses)
        for nut_name, line in self.target_nutr_lines.items():
            line[0].set_data(gens, target_nutrs[nut_name])
        self.fitness_hist_ax.relim()
        self.fitness_hist_ax.autoscale_view()


plotter = Plotter()
plt.show()
