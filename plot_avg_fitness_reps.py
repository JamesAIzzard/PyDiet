import json
from typing import List, Tuple

from matplotlib import pyplot as plt


def process_fitness_data(reps_datafile: str) -> Tuple[List, List]:
    """Processes the fitness data in the specified reps datafile."""

    # Load the data into a dict;
    with open(reps_datafile, 'r') as fh:
        raw_data = fh.read()
        data = json.loads(raw_data)

    # Form an average dataset;
    avg_data = {}
    gen_count = len(data["1"])
    reps = len(data)
    for rep in data:
        for gen in range(2, gen_count + 1):
            # If this is the first pass, initialise the value;
            if gen not in avg_data:
                avg_data[gen] = 0
            avg_data[gen] += data[rep][str(gen)]
    for gen in avg_data:
        avg_data[gen] = avg_data[gen] / reps

    return list(avg_data.keys()), list(avg_data.values())


# Process the data;
gens, A = process_fitness_data('iteration-vs-random-generation-m15-r85.json')
_, B = process_fitness_data('iteration-vs-random-generation-m50-r50.json')
_, C = process_fitness_data('iteration-vs-random-generation-m85-r15.json')
# Draw the plot;
fig = plt.figure(1)
fig.canvas.manager.set_window_title("Average Fitness")
fitness_hist_ax = fig.add_subplot(1, 1, 1)
fitness_hist_ax.set_xlabel('Generation # (u/l)')
fitness_hist_ax.set_ylabel('Fitness Score $\\in$ [0,1] (u/l)')
fitness_hist_ax.grid()
fitness_hist_ax.plot(gens, A, label="A")
fitness_hist_ax.plot(gens, B, label="B")
fitness_hist_ax.plot(gens, C, label="C")
plt.legend()
plt.show()

# POP SIZE VS GENERATIONS
# reps = range(2, 200)
# _, A = process_fitness_data('population-vs-generation-p50-g200.json')
# _, B = process_fitness_data('population-vs-generation-p100-g100.json')
# B = B+100*[None]
# _, C = process_fitness_data('population-vs-generation-p200-g50.json')
# C = C+150*[None]
# # Draw the plot;
# fig = plt.figure(1)
# fig.canvas.manager.set_window_title("Average Fitness")
# fitness_hist_ax = fig.add_subplot(1, 1, 1)
# fitness_hist_ax.set_xlabel('Generation # (u/l)')
# fitness_hist_ax.set_ylabel('Fitness Score $\\in$ [0,1] (u/l)')
# fitness_hist_ax.grid()
# fitness_hist_ax.plot(reps, A, label="A")
# fitness_hist_ax.plot(reps, B, label="B")
# fitness_hist_ax.plot(reps, C, label="C")
# plt.legend()
# plt.show()
