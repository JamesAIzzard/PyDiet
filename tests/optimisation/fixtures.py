"""Fixtures for testing the optimisation module."""

test_ga_configs = {
    "max_population_size": 10000
}

test_constraints = {
    "tags": ["main", "side", "drink"],
    "flags": {
        "vegetarian": True,
        "nut_free": True
    }
}

test_goals = {
    'target_nutrient_masses': {
        "protein": 30,
        "carbohydrate": 40,
        "fat": 30
    },
    'total_calories': 1000,
    'max_cost': 3.00
}