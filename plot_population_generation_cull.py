import json
from matplotlib import pyplot as plt

import numpy as np


def calculate_average_fitness(filename: str = None) -> float:
    # Load the data into a dict;
    with open(filename, 'r') as fh:
        raw_data = fh.read()
        data = json.loads(raw_data)

    avg_fitness = 0
    gens = len(data["1"])
    reps = len(data)
    for rep in data:
        avg_fitness += data[rep][str(gens + 1)]
    avg_fitness = avg_fitness / reps

    return avg_fitness


def create_datafile_name(p: int, g: int, c: int) -> str:
    return f'population-generation-cull-p{p}-g{g}-c{c}.json'


# Calculate the points to check things don't get mixed up
points = [
    ("p50-g50-c25", calculate_average_fitness(filename=create_datafile_name(p=50, g=50, c=25))),
    ("p50-g50-c50", calculate_average_fitness(filename=create_datafile_name(p=50, g=50, c=50))),
    ("p50-g50-c75", calculate_average_fitness(filename=create_datafile_name(p=50, g=50, c=75))),
    ("p50-g200-c25", calculate_average_fitness(filename=create_datafile_name(p=50, g=200, c=25))),
    ("p50-g200-c50", calculate_average_fitness(filename=create_datafile_name(p=50, g=200, c=50))),
    ("p50-g200-c75", calculate_average_fitness(filename=create_datafile_name(p=50, g=200, c=75))),
    ("p100-g100-c25", calculate_average_fitness(filename=create_datafile_name(p=100, g=100, c=25))),
    ("p100-g100-c50", calculate_average_fitness(filename=create_datafile_name(p=100, g=100, c=50))),
    ("p100-g100-c75", calculate_average_fitness(filename=create_datafile_name(p=100, g=100, c=75))),
    ("p125-g125-c25", calculate_average_fitness(filename=create_datafile_name(p=125, g=125, c=25))),
    ("p125-g125-c50", calculate_average_fitness(filename=create_datafile_name(p=125, g=125, c=50))),
    ("p125-g125-c75", calculate_average_fitness(filename=create_datafile_name(p=125, g=125, c=75))),
    ("p200-g50-c25", calculate_average_fitness(filename=create_datafile_name(p=200, g=50, c=25))),
    ("p200-g50-c50", calculate_average_fitness(filename=create_datafile_name(p=200, g=50, c=50))),
    ("p200-g50-c75", calculate_average_fitness(filename=create_datafile_name(p=200, g=50, c=75))),
    ("p200-g200-c25", calculate_average_fitness(filename=create_datafile_name(p=200, g=200, c=25))),
    ("p200-g200-c50", calculate_average_fitness(filename=create_datafile_name(p=200, g=200, c=50))),
    ("p200-g200-c75", calculate_average_fitness(filename=create_datafile_name(p=200, g=200, c=75))),
]

# Draw the plot;
fig = plt.figure(1)
fig.canvas.manager.set_window_title("Generations vs Population vs Cull/%")
domain_ax = fig.add_subplot(1, 1, 1, projection='3d')
P = [50, 50, 50, 50, 50, 50, 125, 125, 125, 200, 200, 200, 200, 200, 200]
G = [50, 50, 50, 200, 200, 200, 125, 125, 125, 50, 50, 50, 200, 200, 200]
C = [25, 50, 75, 25, 50, 75, 25, 50, 75, 25, 50, 75, 25, 50, 75]
F = [
    calculate_average_fitness(filename=create_datafile_name(p=50, g=50, c=25)),
    calculate_average_fitness(filename=create_datafile_name(p=50, g=50, c=50)),
    calculate_average_fitness(filename=create_datafile_name(p=50, g=50, c=75)),
    calculate_average_fitness(filename=create_datafile_name(p=50, g=200, c=25)),
    calculate_average_fitness(filename=create_datafile_name(p=50, g=200, c=50)),
    calculate_average_fitness(filename=create_datafile_name(p=50, g=200, c=75)),
    calculate_average_fitness(filename=create_datafile_name(p=125, g=125, c=25)),
    calculate_average_fitness(filename=create_datafile_name(p=125, g=125, c=50)),
    calculate_average_fitness(filename=create_datafile_name(p=125, g=125, c=75)),
    calculate_average_fitness(filename=create_datafile_name(p=200, g=50, c=25)),
    calculate_average_fitness(filename=create_datafile_name(p=200, g=50, c=50)),
    calculate_average_fitness(filename=create_datafile_name(p=200, g=50, c=75)),
    calculate_average_fitness(filename=create_datafile_name(p=200, g=200, c=25)),
    calculate_average_fitness(filename=create_datafile_name(p=200, g=200, c=50)),
    calculate_average_fitness(filename=create_datafile_name(p=200, g=200, c=75)),
]
domain_ax.set_ylabel('Max Generations')
domain_ax.set_xlabel('Max Population')
domain_ax.set_zlabel('Cull /%')
domain_ax.grid()
img = domain_ax.scatter(P, G, C, c=F, cmap=plt.jet(), edgecolor="black")
plt.colorbar(img)
plt.show()

print(points)