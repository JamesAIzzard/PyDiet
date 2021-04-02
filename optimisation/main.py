from typing import Dict

import goals
from model import meals


def optimise_meal_goals(meal_goals: 'goals.MealGoals') -> 'meals.MealQuantity':
    """Runs the optimisation process against the MealGoals instance provided."""
    # Do stuff...
    return meals.MealQuantity()


def optimise_day_goals(day_goals: 'goals.DayGoals') -> 'Dict[str, meals.MealQuantity]':
    """Runs the optimisation process against the DayGoals instance provided."""
