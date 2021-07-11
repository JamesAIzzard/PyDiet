"""Graphing functionality to display results from the optimiser."""
import copy
import json
from typing import List, Dict

from matplotlib import animation
from matplotlib import pyplot as plt

import model
import optimisation
from optimisation import configs


class Plotter:
    """Provides result plotting functionality."""

    def __init__(
            self,
            target_nutrient_ratios: Dict[str, float] = configs.goals['target_nutrient_ratios'],
            max_cost: float = configs.goals['max_cost']
    ):
        # Configure the plot;
        self.fig = plt.figure(1)
        plt.subplots_adjust(
            left=0.08,
            bottom=0.1,
            right=0.85,
            top=0.95,
            wspace=0.2,
            hspace=0.2)
        self.fig.canvas.manager.set_window_title("PyDiet")
        self.fitness_hist_ax = self.fig.add_subplot(1, 1, 1)
        self.target_ratio_ax = self.fitness_hist_ax.twinx()
        self.target_ratio_ax.set_ylim((0, 1))
        self.target_ratio_ax.set_ylabel('Target Nutrient Ratios (u/l)')
        self.cost_ax = self.fitness_hist_ax.twinx()
        self.cost_ax.spines['right'].set_position(('axes', 1.1))
        self.cost_ax.set_ylim((0, max_cost))
        self.cost_ax.set_ylabel('Cost of Meal (£GBP)')
        self.fitness_hist_ax.set_xlabel('Generation # (u/l)')
        self.fitness_hist_ax.set_ylabel('Fitness Score $\\in$ [0,1] (u/l)')
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
        self.cost_hist_line, = self.cost_ax.plot(
            [], [],
            color="g",
            label="cost",
            linestyle='--'
        )
        self.target_nutr_lines = {}
        for nutr_name in target_nutrient_ratios.keys():
            # Horizontal lines marking targets.
            # _ = self.target_ratio_ax.axhline(
            #     y=target_nutrient_ratios[nutr_name],
            #     linestyle='--',
            #     color="black",
            #     linewidth=1
            # )
            self.target_nutr_lines[nutr_name] = self.target_ratio_ax.plot(
                [], [],
                label=nutr_name
            )
        fh_lines, fh_labels = self.fitness_hist_ax.get_legend_handles_labels()
        cn_lines, cn_labels = self.cost_ax.get_legend_handles_labels()
        tn_lines, tn_labels = self.target_ratio_ax.get_legend_handles_labels()
        lines = fh_lines + tn_lines + cn_lines
        labels = fh_labels + tn_labels + cn_labels
        plt.legend(lines, labels, loc=2)
        self._ani = animation.FuncAnimation(self.fig, self.run, interval=500, repeat=True)

    def run(self, _):
        """Update function."""
        # Create lists for the data;
        gens = []
        fitnesses = []
        target_nutrs = {nut_name: [] for nut_name in self.target_nutr_lines.keys()}
        costs_gbp: List[float] = []

        # Open the logfile and read the data;
        with open(configs.history_path, 'r') as fh:
            raw_data = fh.read()
            data = json.loads(raw_data)
        # Work through each entry in the data;
        for row in data:
            # Grab the generation number;
            gens.append(row[0])

            cost = row[1]['cost']
            fitness = row[1]['fitness']

            # Create a meal instance from the data;
            # First grab the meal data;
            md = copy.copy(row[1])
            del md['nutrient_ratios']
            del md['fitness']
            del md['cost']
            del md['ingredient_quantities']
            m = model.meals.SettableMeal(meal_data=md)

            # Calculate the fitness of the instance;
            fitnesses.append(fitness)

            # Append the nutreint ratios to their respective datalines;
            for nut_name in self.target_nutr_lines.keys():
                target_nutrs[nut_name].append(m.get_nutrient_ratio(nut_name).subject_g_per_host_g)

            # Append the cost;
            costs_gbp.append(cost)

        self.fitness_hist_line.set_data(gens, fitnesses)
        self.cost_hist_line.set_data(gens, costs_gbp)
        for nut_name, line in self.target_nutr_lines.items():
            line[0].set_data(gens, target_nutrs[nut_name])

        self.fitness_hist_ax.relim()
        self.fitness_hist_ax.autoscale_view()


plotter = Plotter()
plt.show()
