"""Defines recipe quantity classes."""
import model


class RecipeQuanityBase:
    """Base class for recipe quantity classes."""
    def __init__(self, recipe: 'model.recipes.ReadonlyRecipe'):
        """Base for recipe quantity classes."""
        # Check the recipe is readonly;
        if not isinstance(recipe, model.recipes.ReadonlyRecipe):
            raise TypeError("Recipe used in quantity must be readonly.")

        # Pass the call on;
        super().__init__(qty_subject=recipe)


class ReadonlyRecipeQuantity(RecipeQuanityBase, model.quantity.IsReadonlyQuantityOf):
    """Models a readonly recipe quantity."""


class SettableRecipeQuantity(RecipeQuanityBase, model.quantity.IsSettableQuantityOf):
    """Models a settable quantity of."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)