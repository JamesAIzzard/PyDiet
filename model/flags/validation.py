from typing import Optional

from model import flags


def validate_flag_name(flag_name: str) -> str:
    """Returns validated flag name or raises exception.
    Raises:
        FlagNameError: To indicate the flag name is not recognised.
    """
    if flag_name in flags.configs.flag_data.keys():
        return str(flag_name)
    raise flags.exceptions.FlagNameError


def validate_flag_value(flag_value: Optional[bool]) -> Optional[bool]:
    """Returns validated flag value or raises exception.
    Raises:
        FlagValueError: To indicate the flag value is not valid.
    """
    if flag_value in [True, False, None]:
        return flag_value
    raise flags.exceptions.FlagValueError
