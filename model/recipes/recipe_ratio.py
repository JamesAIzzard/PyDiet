"""Defines classes modelling recipe ratio functionality."""
import abc

import model
import persistence


class RecipeRatioBase(
    model.quantity.IsQuantityRatioBase,
    persistence.YieldsPersistableData,
    abc.ABC
):
    """Abstract base class for readonly and writable recipe ratios."""

    def __init__(self, recipe: 'model.recipes.ReadonlyRecipe', **kwargs):
        # Check the recipe is a ReadonlyRecipe;
        if not isinstance(recipe, model.recipes.ReadonlyRecipe):
            raise TypeError("Recipe arg must be a ReadonlyRecipe instance.")

        # Pass recipe on to quantity class;
        super().__init__(ratio_subject=recipe, **kwargs)


class ReadonlyRecipeRatio(RecipeRatioBase, model.quantity.IsReadonlyQuantityRatio):
    """Models a readonly recipe ratio."""


class SettableRecipeRatio(RecipeRatioBase, model.quantity.IsSettableQuantityRatio):
    """Models a readable recipe ratio."""
