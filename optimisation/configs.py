"""Configuration file for the optimisation module."""
history_path = "optimisation/history.json"

ga_configs = {
    "max_population_size": 100,
    "acceptable_fitness": 0.95,
    "max_generations": 1000,
    "cull_percentage": 70,
    "mutation_probability_percentage": 50,
    "random_solution_intro_percentage": 10,
    "log_every_n_updates": 10,
}

constraints = {
    "tags": ["main", "side", "drink"],
    "flags": {
        "vegetarian": True,
        "nut_free": True
    }
}

goals = {
    'target_nutrient_ratios': {
        "protein": 0.3,
        "carbohydrate": 0.3,
        "fat": 0.4,
        "saturated_fat": 0.3,
    },
    'total_calories': 1000,
    'max_cost': 4.00
}