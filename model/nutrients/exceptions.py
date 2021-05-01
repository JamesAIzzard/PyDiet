from typing import Union, Optional

import model


class BaseNutrientError(model.exceptions.PyDietModelError):
    """Base class for all nutrient related exceptions."""

    def __init__(self, subject: Optional[Union[
        'model.nutrients.NutrientRatioData',
        'model.nutrients.NutrientRatio',
        'model.nutrients.SettableNutrientRatio',
        'model.nutrients.HasNutrientRatios',
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


class NutrientRatioNotSettableError(NamedNutrientError):
    """Indicating the subject does not support nutrient ratio setting."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class NutrientQtyExceedsSubjectQtyError(NamedNutrientError):
    """Indicates the nutrient quantity exceeds the ingredient quantity."""

    def __init__(self,
                 nutrient_qty: float,
                 nutrient_qty_units: str,
                 subject_qty: float,
                 subject_qty_units: str, **kwargs):
        super().__init__(**kwargs)
        self.nutrient_qty = nutrient_qty
        self.nutrient_qty_units = nutrient_qty_units
        self.subject_qty = subject_qty
        self.subject_qty_units = subject_qty_units


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
