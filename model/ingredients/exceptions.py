from typing import Optional

import model


class BaseIngredientError(model.exceptions.PyDietModelError):
    """Base exception for all ingredient errors."""

    def __init__(self, ingredient: Optional['model.ingredients.Ingredient'] = None):
        self.ingredient = ingredient
