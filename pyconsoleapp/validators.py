from typing import Tuple

import pyconsoleapp


def validate_integer(value) -> int:
    """Raises ResponseValidationError if value is not an integer. Otherwise returns integer value."""
    try:
        int_value = int(value)
    except ValueError:
        raise pyconsoleapp.ResponseValidationError('Input must be an integer.')
    return int_value


def validate_number(value) -> float:
    """Raises ResponseValidationError if value is not a float. Otherwise returns value as float."""
    try:
        value = float(value)
    except ValueError:
        raise pyconsoleapp.ResponseValidationError('Input must be a number.')
    return value


def validate_positive_nonzero_number(value) -> float:
    """Raises ResponseValidationError if value is not a positive non-zero number. Otherwise returns value as float."""
    value = validate_number(value)
    if value <= 0:
        raise pyconsoleapp.ResponseValidationError('Input must be a number > 0.')
    return value


def validate_positive_or_zero_number(value) -> float:
    value = validate_number(value)
    if value < 0:
        raise pyconsoleapp.ResponseValidationError('Input must be a number > 0.')
    return value


def validate_number_and_str(value) -> Tuple[float, str]:
    text = value.strip('0123456789.')
    num = value.strip(text)
    try:
        num = validate_number(num)
    except pyconsoleapp.ResponseValidationError:
        raise pyconsoleapp.ResponseValidationError('Input must be a number followed by text.')
    return num, text
