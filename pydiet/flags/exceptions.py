import pydiet


class FlagNutrientConflictError(pydiet.exceptions.PyDietException):
    """The flag value conflicts with the nutrient data."""


class FlagNameError(pydiet.exceptions.PyDietException):
    """The flag name is not recognised."""


class FlagValueError(pydiet.PyDietException):
    """The flag value is not True, False or None."""
