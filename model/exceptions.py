from typing import Optional, List, Any

import model


class PyDietModelError(Exception):
    """Base exception for all exceptions raised by the model."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UndefinedNameError(PyDietModelError):
    """Indicates the instance name is not defined."""

    def __init__(self, subject: Any, **kwargs):
        super().__init__(**kwargs)
        self.subject = subject


class NutrientRatioConflictError(PyDietModelError):
    """Base exception for nutrient-flag conflicts."""

    def __init__(self,
                 flag_name: str, flag_value: Optional[bool],
                 conflicting_nutrient_ratios: List['model.nutrients.NutrientRatio'],
                 **kwargs
                 ):
        super().__init__(**kwargs)
        self.flag_name = flag_name
        self.flag_value = flag_value
        self.conflicting_nutrient_ratios = conflicting_nutrient_ratios


class TerminalNutrientRatioConflictError(NutrientRatioConflictError):
    """Indicates there is a nutrient ratio conflict which can't be fixed automatically."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class FixableNutrientRatioConflictError(NutrientRatioConflictError):
    """Indicates there is a nutrient ratio conflict which can be fixed automatically."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class NonZeroNutrientRatioConflictError(TerminalNutrientRatioConflictError):
    """Indicates nutrient ratios have to be non-zero for a flag to apply. We can't set them to non-zero
    because we don't know what their specific values are."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UndefineMultipleNutrientRatiosError(TerminalNutrientRatioConflictError):
    """Indicates the flag being undefined is a direct alias for a group of nutrient ratios that are all
    defined. We don't know which to undefine to release the flag value to undefined."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class PercentageSumError(PyDietModelError, ValueError):
    """Indicating the set of percentages do not sum to 100%."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class InvalidPercentageValueError(PyDietModelError, ValueError):
    """Indicating the percentage value is not in [0-100]."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
