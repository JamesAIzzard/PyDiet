"""Test fixtures for the recipe module."""
from typing import Optional

import model


class RecipeBaseTestable(model.recipes.RecipeBase):
    """Minimal implementation to allow testing of RecipeBase class."""

    def __init__(self, recipe_data: 'model.recipes.RecipeData'):
        super().__init__()
        self._recipe_data = recipe_data

    @property
    def _name(self) -> Optional[str]:
        """Returns the recipe name."""
        return self._recipe_data['name']
