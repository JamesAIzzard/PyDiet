"""Test fixtures for the recipe module."""
import model


class RecipeBaseTestable(model.recipes.RecipeBase):
    """Minimal implementation to allow testing of RecipeBase class."""
    pass
