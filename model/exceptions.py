class PyDietException(Exception):
    """Base exception for the PyDiet application."""


class FlagNutrientConflictError(PyDietException):
    """Indicating a conflict between flag data and nutrient ratio data."""


class PercentageSumError(PyDietException, ValueError):
    """Indicating the set of percentages do not sum to 100%."""


class InvalidPercentageValueError(PyDietException, ValueError):
    """Indicating the percentage value is not in [0-100]."""
