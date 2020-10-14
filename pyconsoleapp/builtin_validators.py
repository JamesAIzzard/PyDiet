from typing import Any, Tuple

from pyconsoleapp import ResponseValidationError


def validate_integer(value: Any) -> int:
    try:
        int_value = int(value)
    except TypeError:
        raise ResponseValidationError('Input must be an integer.')
    return int_value


def validate_positive_nonzero_number(value: Any) -> float:
    try:
        value = float(value)
    except ValueError:
        raise ResponseValidationError('Input must be a number.')
    if value <= 0:
        raise ResponseValidationError('Input must be a number > 0.')
    return value


def validate_positive_or_zero_number(value: Any) -> float:
    try:
        value = float(value)
    except ValueError:
        raise ResponseValidationError('Input must be a number.')
    if value < 0:
        raise ResponseValidationError('Input must be a number > 0.')
    return value


def validate_number_and_str(value: str) -> Tuple[float, str]:
    text = value.strip('0123456789.')
    num = value.strip(text)
    try:
        num = float(num)
    except ValueError:
        raise ResponseValidationError('Input must be a number followed by text.')
    return num, text
