from typing import Union, Optional, Any

import model


class BaseFlagError(model.exceptions.PyDietModelError):
    """Base class for flag related exceptions."""

    def __init__(self,
                 subject: Optional[Union[
                     'model.flags.HasFlags',
                     'model.flags.HasSettableFlags']
                 ] = None, **kwargs):
        super().__init__(**kwargs)
        self.subject = subject


class FlagNameError(BaseFlagError):
    """The flag name is not recognised."""

    def __init__(self, flag_name: str, **kwargs):
        super().__init__(**kwargs)
        self.flag_name = flag_name


class FlagValueError(BaseFlagError, ValueError):
    """The flag qty is not True, False or None."""

    def __init__(self, value: Any, **kwargs):
        super().__init__(**kwargs)
        self.flag_value = value


class UnexpectedFlagDOFError(BaseFlagError):
    """Indicates data is stored against a flag DOF where the flag is a direct alias, and therefore
    should only rely on the state of nutrient ratios."""

    def __init__(self, flag_name: str, **kwargs):
        super().__init__(**kwargs)
        self.flag_name = flag_name


class FlagHasNoDOFError(BaseFlagError):
    """Indicates the flag is unexpectedly missing a degree of freedom."""

    def __init__(self, flag_name: str, **kwargs):
        super().__init__(**kwargs)
        self.flag_name = flag_name


class UndefinedFlagError(BaseFlagError):
    """Indicates the flag value is not defined;"""

    def __init__(self, flag_name: str, reason: str, **kwargs):
        super().__init__(**kwargs)
        self.flag_name = flag_name
        self.reason = reason
