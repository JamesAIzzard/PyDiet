import model


class BaseRecipeError(model.exceptions.PyDietModelError):
    """Base error for the recipe module"""

    def __init__(self, subject: 'model.recipes.RecipeBase', **kwargs):
        super().__init__(**kwargs)
        self.subject = subject


class IngredientNotInRecipeError(BaseRecipeError):
    """Indicates the ingredient specified is not included in the recipe's ingredient amount list."""

    def __init__(self, ingredient_name: str, **kwargs):
        super().__init__(**kwargs)
        self.ingredient_name = ingredient_name
