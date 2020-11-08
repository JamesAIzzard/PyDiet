from pydiet.exceptions import PyDietException


class FlagNutrientConflictError(PyDietException):
    """The flag qty conflicts with the nutrient data."""


class FlagNameError(PyDietException):
    """The flag name is not recognised."""


class FlagValueError(PyDietException):
    """The flag qty is not True, False or None."""
