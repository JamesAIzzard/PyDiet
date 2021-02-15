from model.exceptions import PyDietException


class ReadonlyNutrientRatioError(PyDietException):
    """Indicating the object does not support setting nutrient ratios."""


class NutrientConfigsError(PyDietException):
    """Indicates a general error with the nutrient configuration file."""


class NutrientNameError(PyDietException):
    """Indicates a general error relating to nutrient naming."""


class NutrientRatioGroupError(PyDietException):
    """Indicates the group of nutrient ratios are collectively invalid."""


class NutrientQtyExceedsSubjectQtyError(NutrientRatioGroupError):
    """Indicates the nutrient quantity exceeds the ingredient quantity."""


class ChildNutrientQtyExceedsParentNutrientQtyError(NutrientRatioGroupError):
    """Indicates the child nutrient quantity exceeds the parent nutrient quantity."""
