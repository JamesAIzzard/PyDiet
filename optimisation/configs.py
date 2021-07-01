"""Configuration file for the optimisation module."""
history_path = "optimisation/history.json"

ga_configs = {
    "max_population_size": 1000,
    "acceptable_fitness": 0.95,
    "max_generations": 100,
    "cull_percentage": 70,
    "mutation_probability_percentage": 50,
    "random_solution_intro_percentage": 90,
    "log_every_n_updates": 100,
}

constraints = {
    "tags": ["main", "side", "drink"],
    "flags": {
        "vegetarian": True,
        "nut_free": True
    }
}

goals = {
    'target_nutrient_masses': {
        "protein": 40,
        "carbohydrate": 60,
        "fat": 10
    },
    'total_calories': 1000,
    'max_cost': 3.00
}