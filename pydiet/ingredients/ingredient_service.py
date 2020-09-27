from typing import TYPE_CHECKING, List

from pydiet import ingredients

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient


def load_new_ingredient() -> 'Ingredient':
    """Creates and returns a fresh ingredient instance with no data filled in."""
    return ingredients.ingredient.Ingredient(
        ingredients.ingredient.get_empty_ingredient_data())

