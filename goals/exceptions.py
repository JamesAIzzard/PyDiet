from typing import Optional

import exceptions
import goals
import model


class BaseGoalError(exceptions.PyDietError):
    """Base exception for all goal module exceptions."""

    def __init__(self, subject: Optional['goals.HasSettableGoals'], **kwargs):
        super().__init__(**kwargs)
        self.subject = subject


class MealGoalNameClashError(BaseGoalError):
    """Indicates two MealGoal instances with the same name are attemping to be added
    to the DayGoals instance."""

    def __init__(self, clashing_name: str, **kwargs):
        super().__init__(**kwargs)
        self.name = clashing_name


class UndefinedMealGoalNameError(BaseGoalError):
    """Indicates the MealGoals instance is not named."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UndefinedMaxCostTargetError(BaseGoalError):
    """Indicates the max cost target is not defined."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UndefinedMealTimeError(BaseGoalError):
    """Indicates the max cost target is not defined."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UndefinedCalorieTargetError(BaseGoalError):
    """Indicates the calorie target is not defined."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class NutrientMassGoalError(BaseGoalError, model.nutrients.exceptions.NamedNutrientError):
    """Indicates there is some error relating to a nutrient mass goal"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UndefinedNutrientMassGoalError(NutrientMassGoalError, model.nutrients.exceptions.UndefinedNutrientMassError):
    """Indicates the nutrient does not have a mass goal defined."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ConflictingNutrientMassGoalError(NutrientMassGoalError):
    """Conflict between DayGoals nutrient mass target and one of its child MealGoals
    targets for the same nutrient."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class OverConstrainedNutrientMassGoalError(NutrientMassGoalError):
    """Indicates a nutrient mass goal is being set on a DayGoal instance when it is
    already completely constrained by the child MealGoal instances."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UndefinedParentDayGoalError(BaseGoalError):
    """Indicates there is no parent DayGoals instance."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
