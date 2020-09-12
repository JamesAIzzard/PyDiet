from pyconsoleapp.exceptions import ResponseValidationError
from typing import Any, Tuple

from pyconsoleapp import exceptions


def validate_integer(value: Any) -> int:
    try:
        int_value = int(value)
    except TypeError:
        raise exceptions.ResponseValidationError('Input must be an integer.')
    return int_value


def validate_positive_nonzero_number(value: Any) -> float:
    try:
        value = float(value)
    except TypeError:
        raise exceptions.ResponseValidationError
    if value <= 0:
        raise exceptions.ResponseValidationError('Input must be a number > 0.')    
    return value
