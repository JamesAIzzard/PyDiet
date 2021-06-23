"""Defines meal classes."""
from typing import List, Dict, Callable, Optional, Any

import model
import persistence


class SettableMeal(
    model.recipes.HasSettableRecipeQuantities,
    persistence.YieldsPersistableData,
    persistence.CanLoadData
):
    """Models a collection of recipes (combined to form a meal)."""

    def __init__(self, meal_data: Optional['model.meals.MealData'] = None):

        # Stash the meal data passed in during init;
        self._meal_data = {}

        if meal_data is not None:
            self.load_data(meal_data)

    @property
    def persistable_data(self) -> Dict[str, Any]:
        """Returns the persistable data for this meal instance."""
        return self._meal_data

    def load_data(self, meal_data: 'model.meals.MealData') -> None:
        """Loads data into the instance."""
        self._meal_data = meal_data
