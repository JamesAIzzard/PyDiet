"""Defines recipe quantity classes."""
import abc
from typing import Dict, Any

import model
import persistence
from .recipe_ratio import HasReadableRecipeRatios


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


class HasSettableRecipeQuantities(
    HasReadableRecipeRatios,
    model.ingredients.HasReadableIngredientQuantities,
    persistence.YieldsPersistableData,
    abc.ABC
):
    """Mixin to implement functionality associated with settable recipe quantities."""

    @property
    @abc.abstractmethod
    def recipe_quantities_data(self) -> 'model.recipes.RecipeQuantitiesData':
        """Returns the recipe quantities data for this instance."""
        raise NotImplementedError

    @property
    def ingredient_quantities_data(self) -> 'model.ingredients.IngredientQuantitiesData':
        """Returns the ingredient quantities data for this instance."""
        raise NotImplementedError

    @property
    def recipe_quantities(self) -> Dict[str, 'model.recipes.ReadonlyRecipeQuantity']:
        """Returns the recipe quantities associated with this instance."""
        raise NotImplementedError

    @property
    def persistable_data(self) -> Dict[str, Any]:
        """Returns the instance's persistable data."""
        raise NotImplementedError
