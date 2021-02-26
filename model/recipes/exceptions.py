from model.exceptions import PyDietException


class IngredientNotInRecipeError(PyDietException):
    """Indicates the ingredient is not included in the recipe's ingredient amount list."""
