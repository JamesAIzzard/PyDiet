from typing import List, Optional

from model import nutrients
from model.exceptions import PyDietException


class FlagNameError(PyDietException):
    """The flag name is not recognised."""


class FlagValueError(PyDietException):
    """The flag qty is not True, False or None."""


class UnexpectedFlagDOFError(PyDietException):
    """Indicates data is stored against a flag DOF where the flag is a direct alias, and therefore
    should only rely on the state of nutrient ratios."""

    def __init__(self, flag_name: str):
        self.flag_name = flag_name


class FlagHasNoDOFError(PyDietException):
    """Indicates the flag does not have a DOF."""

    def __init__(self, flag_name: str):
        self.flag_name = flag_name


class NutrientRatioConflictError(PyDietException):
    """Base exception which indicates setting a flag to a specific value would
    cause conflict between flags and nutrients ratios on the instance."""

    def __init__(self, flag_name: str, flag_value: Optional[bool],
                 conflicting_nutrient_ratios: List['nutrients.NutrientRatio']):
        self.flag_name = flag_name
        self.flag_value = flag_value
        self.conflicting_nutrient_ratios = conflicting_nutrient_ratios


class NonZeroNutrientRatioConflictError(NutrientRatioConflictError):
    """Indicates nutrient ratios have to be non-zero for a flag to apply. We can't set them to non-zero
    because we don't know what their specific values are."""


class UndefineMultipleNutrientRatiosError(NutrientRatioConflictError):
    """Indicates the flag being undefined is a direct alias for a group of nutrient ratios that are all
    defined. We don't know which to undefine to release the flag value to undefined."""


class FixableNutrientRatioConflictError(NutrientRatioConflictError):
    """Indicates there are conflicts with the nutrient ratios that can be fixed automatically."""
