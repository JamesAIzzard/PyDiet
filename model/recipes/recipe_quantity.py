"""Defines recipe quantity classes."""
import abc

import model


class RecipeQuantityBase(model.quantity.IsQuantityOfBase, abc.ABC):
    """Base class for recipe quantity classes."""

    def __init__(self, recipe: 'model.recipes.ReadonlyRecipe', **kwargs):
        """Base for recipe quantity classes."""
        # Check the recipe is readonly;
        if not isinstance(recipe, model.recipes.ReadonlyRecipe):
            raise TypeError("Recipe used in quantity must be readonly.")

        # Pass the call on;
        super().__init__(qty_subject=recipe, **kwargs)

    @property
    def recipe(self) -> 'model.recipes.ReadonlyRecipe':
        """Returns the recipe instance.
        Alias for qty_subject."""
        return self.qty_subject


class ReadonlyRecipeQuantity(RecipeQuantityBase, model.quantity.IsReadonlyQuantityOf):
    """Models a readonly recipe quantity."""


class SettableRecipeQuantity(RecipeQuantityBase, model.quantity.IsSettableQuantityOf):
    """Models a settable quantity of."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
