"""Configuration file for the optimisation module."""
history_path = "optimisation/history.json"

ga_configs = {
    "max_population_size": 50,
    "acceptable_fitness": 0.95,
    "max_generations": 200,
    "cull_percentage": 25,
    "mutation_probability_percentage": 50,
    "random_solution_intro_percentage": 50,
    "log_every_n_updates": 10,
}

constraints = {
    "tags": ["main", "side"],
    "flags": {
        "vegetarian": True,
        "nut_free": True
    },
    "time": "20:00"
}

goals = {
    'target_nutrient_ratios': {
        "protein": 0.1,
        "carbohydrate": 0.5,
        "fat": 0.2,
        "saturated_fat": 0.05,
    },
    'total_calories': 1000,
    'max_cost': 4.00
}