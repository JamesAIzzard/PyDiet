from model.exceptions import PyDietException


class ConflictingNutrientMassGoalError(PyDietException):
    """Conflict between DayGoals nutrient mass target and one of its child MealGoals
    targets for the same nutrient."""


class OverConstrainedNutrientMassGoalError(PyDietException):
    """Indicates a nutrient mass goal is being set on a DayGoal instance when it is
    already completely constrained by the child MealGoal instances."""


class MealGoalNameClashError(PyDietException):
    """Indicates two MealGoal instances with the same name are attemping to be added
    to the DayGoals instance."""


class UnnamedMealGoalError(PyDietException):
    """Indicates the MealGoals instance is not named, and needs to be."""
