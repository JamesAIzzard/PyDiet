import model
from . import exceptions


def validate_flag_name(flag_name: str) -> str:
    """Returns validated flag name or raises exception.
    Raises:
        FlagNameError: To indicate the flag name is not recognised.
    """
    if flag_name in model.flags.ALL_FLAGS.keys():
        return str(flag_name)
    raise exceptions.FlagNameError(flag_name=flag_name)


def validate_flag_value(flag_value: bool) -> bool:
    """Returns validated flag value or raises exception.
    Raises:
        FlagValueError: To indicate the flag value is not valid.
    """
    if flag_value in [True, False]:
        return flag_value
    raise exceptions.FlagValueError(value=flag_value)
