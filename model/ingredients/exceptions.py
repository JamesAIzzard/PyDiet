"""Exceptions for the ingredient module."""
from typing import Optional

import model


class BaseIngredientError(model.exceptions.PyDietModelError):
    """Base exception for all ingredient errors."""

    def __init__(self, ingredient: Optional['model.ingredients.ReadonlyIngredient'] = None):
        self.ingredient = ingredient


class IngredientRatiosSumExceedsOneError(BaseIngredientError):
    """Indicates the sum of the ingredient ratios exceeds one."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
