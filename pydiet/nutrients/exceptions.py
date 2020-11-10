from pydiet.exceptions import PyDietException


class NutrientRatioNotSettableError(PyDietException):
    """Indicating the object does not support setting nutrient ratios."""


class NutrientConfigsError(PyDietException):
    """Indicates a general error with the nutrient configuration file."""


class NutrientNameError(PyDietException):
    """Indicates a general error relating to nutrient naming."""


class InvalidNutrientQtyError(PyDietException):
    """Indicates the nutrient amount is not valid."""


class NutrientQtyExceedsIngredientQtyError(InvalidNutrientQtyError):
    """Indicates the nutrient quantity exceeds the ingredient quantity."""


class ChildNutrientQtyExceedsParentNutrientQtyError(InvalidNutrientQtyError):
    """Indicates the child nutrient quantity exceeds the parent nutrient quantity."""
