"""Defines exception classes for the nutrients module."""
from typing import Union, Optional

import model


class BaseNutrientError(model.exceptions.PyDietModelError):
    """Base class for all nutrient related exceptions."""

    def __init__(self, subject: Optional[Union[
        'model.nutrients.NutrientRatioData',
        'model.nutrients.ReadonlyNutrientRatio',
        'model.nutrients.SettableNutrientRatio',
        'model.nutrients.HasReadableNutrientRatios',
        'model.nutrients.HasSettableNutrientRatios'
    ]] = None, **kwargs):
        super().__init__(**kwargs)
        self.subject = subject


class NamedNutrientError(BaseNutrientError):
    """Base class for all nutrient exceptions."""

    def __init__(self, nutrient_name: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.nutrient_name = nutrient_name


# General Nutrient Exceptions
# -------------------------------------------------

class NutrientConfigsError(BaseNutrientError):
    """Indicates a error with the nutrient configuration file."""

    def __init__(self, error_msg: str, **kwargs):
        super().__init__(**kwargs)
        self.error_msg = error_msg


class NutrientNameNotRecognisedError(NamedNutrientError):
    """Indicates a general error relating to nutrient naming."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# Nutrient Ratio Exceptions
# -------------------------------------------------

class UndefinedNutrientRatioError(NamedNutrientError):
    """Indicates the nutrient ratio is not defined on the instance."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UndefinedCalorieNutrientRatioError(UndefinedNutrientRatioError):
    """Indicates that a nutrient ratio required to calculate the caloric density is undefined."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class NutrientRatioNotSettableError(NamedNutrientError):
    """Indicating the subject does not support nutrient ratio setting."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class NutrientMassExceedsSubjectQtyError(NamedNutrientError):
    """Indicates the nutrient quantity exceeds the ingredient quantity."""

    def __init__(self,
                 nutrient_mass_value: float,
                 nutrient_mass_units: str,
                 host_qty_value: float,
                 host_qty_units: str, **kwargs):
        super().__init__(**kwargs)
        self.nutrient_mass = nutrient_mass_value
        self.nutrient_mass_units = nutrient_mass_units
        self.host_qty = host_qty_value
        self.host_qty_units = host_qty_units


# Nutrient Mass Exceptions
# -------------------------------------------------

class UndefinedNutrientMassError(NamedNutrientError):
    """Indicates the nutrient mass is not defined on the instance."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ChildNutrientExceedsParentMassError(BaseNutrientError):
    """Indicates a child nutrient exceeds the mass of one of its parents."""

    def __init__(self, nutrient_group_name: str, **kwargs):
        super().__init__(**kwargs)
        self.nutrient_group_name = nutrient_group_name
