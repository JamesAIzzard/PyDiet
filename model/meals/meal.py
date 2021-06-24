"""Defines meal classes."""
from typing import List, Dict, Callable, Optional, Any

import model
import persistence


class SettableMeal(
    model.recipes.HasSettableRecipeQuantities,
    persistence.YieldsPersistableData,
):
    """Models a collection of recipes (combined to form a meal)."""

    def __init__(self, meal_data: Optional['model.meals.MealData'] = None, **kwargs):
        super().__init__(recipe_quantities_data=meal_data, **kwargs)

    @property
    def persistable_data(self) -> Dict[str, Any]:
        """Returns the persistable data for this meal instance."""
        return self._recipe_quantities_data
