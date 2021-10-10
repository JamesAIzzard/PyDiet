import json
from typing import Dict, TypedDict

import numpy as np
import matplotlib.pyplot as plt


class Result(TypedDict):
    mean: float
    sdev: float


# Create somewhere to store the analysed data;
results: Dict[int, Result] = {}

# Analyse the data;
for p_number in range(1, 11):
    # Load the problem raw datafile;
    with open(f'config{p_number}.json', 'r') as fh:
        data = json.loads(fh.read())

    # Grab the number of repetitions;
    rep_count = len(data)

    # Grab the number of generations;
    gen_count = len(data["1"]) + 1

    # Grab the final scores from each rep;
    final_scores = []
    for r_number in range(1, rep_count + 1):
        final_scores.append(data[str(r_number)][str(gen_count)])

    # Calculate the mean score;
    results[p_number] = Result(
        mean=float(np.mean(final_scores)),
        sdev=float(np.std(final_scores))
    )

# Plot the data;
names = []
means = []
sdevs = []
for p_num, result in results.items():
    names.append(f'Problem {p_num}')
    means.append(result['mean'])
    sdevs.append(result['sdev'])

fig, ax = plt.subplots()
xpos = range(1, 11)
ax.bar(xpos, means, yerr=sdevs, align='center')
ax.set_ylabel('Mean Fitness Score (unitless ratio)')
ax.set_xticks(xpos)
ax.set_xticklabels(names)
ax.yaxis.grid(True)
ax.set_ylim(0.8, 1)
plt.xticks(rotation=90)
plt.show()
