from model.exceptions import PyDietException


class ReadonlyNutrientRatioError(PyDietException):
    """Indicating the object does not support setting nutrient ratios."""


class NutrientConfigsError(PyDietException):
    """Indicates a general error with the nutrient configuration file."""


class NutrientNameError(PyDietException):
    """Indicates a general error relating to nutrient naming."""


class NutrientRatioGroupError(PyDietException):
    """Indicates the group of nutrient ratios are collectively invalid."""


class NutrientQtyExceedsSubjectQtyError(PyDietException):
    """Indicates the nutrient quantity exceeds the ingredient quantity."""

    def __init__(self, nutrient_name: str):
        self.nutrient_name = nutrient_name


class ChildNutrientQtyExceedsParentNutrientQtyError(NutrientRatioGroupError):
    """Indicates the child nutrient quantity exceeds the parent nutrient quantity."""

    def __init__(self, nutrient_group_name: str):
        self.nutrient_group_name = nutrient_group_name
