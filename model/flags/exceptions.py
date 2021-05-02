from typing import Optional, Any

import model


class BaseFlagError(model.exceptions.PyDietModelError):
    """Base class for flag related exceptions."""

    def __init__(self, subject: Any = None, flag_name: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.subject = subject
        self.flag_name = flag_name


class FlagNameError(BaseFlagError):
    """The flag name is not recognised."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class FlagValueError(BaseFlagError, ValueError):
    """The flag qty is not True, False or None."""

    def __init__(self, value: Any, **kwargs):
        super().__init__(**kwargs)
        self.flag_value = value


class UnexpectedFlagDOFError(BaseFlagError):
    """Indicates data is stored against a flag DOF where the flag is a direct alias, and therefore
    should only rely on the state of nutrient ratios."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class FlagHasNoDOFError(BaseFlagError):
    """Indicates the flag is unexpectedly missing a degree of freedom."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UndefinedFlagError(BaseFlagError):
    """Indicates the flag value is not defined;"""

    def __init__(self, reason: str, **kwargs):
        super().__init__(**kwargs)
        self.reason = reason


class NutrientNotRelatedError(BaseFlagError):
    """Indicates the named nutrient is not related to the flag;"""

    def __init__(self, nutrient_name: str, **kwargs):
        super().__init__(**kwargs)
        self.nutrient_name = nutrient_name
