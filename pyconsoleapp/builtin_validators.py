from pyconsoleapp.exceptions import ResponseValidationError
from typing import Any, Tuple

from pyconsoleapp import exceptions


def validate_integer(value: Any) -> int:
    try:
        int_value = int(value)
    except TypeError:
        raise exceptions.ResponseValidationError
    return int_value


def validate_number_and_text(qty_and_text: Any) -> Tuple[float, str]:
    '''Parses a string made up of a number and text. Returns
    the two components seperately as a tuple, number first.

    Args:
        qty_and_text (str): String to parse.

    Returns:
        Tuple[float, str]: Number and text element, seperately
            in a tuple.
    '''
    output = None
    # Strip any initial whitespace;
    qty_and_text = qty_and_text.replace(' ', '')
    # Work along the string until you find something which is
    # not a number;
    for i, char in enumerate(qty_and_text):
        # If char cannot be parsed as a number,
        # split the string here;
        if not char.isnumeric() and not char == '.':
            number_part = float(qty_and_text[:i])
            text_part = str(qty_and_text[i:])
            output = (number_part, text_part)
            break
    if not output:
        raise exceptions.ResponseValidationError('Unable to parse {} into a number and text.'
                                                 .format(qty_and_text))
    # Return tuple;
    return output


def validate_letter_and_integer(chars_to_parse: str) -> Tuple[str, int]:
    '''Parses a string whose first character is a letter, and
    whose following characters form an integer, into a tuple
    containing a letter and an integer.

    Arguments:
        chars_to_parse {str} -- Characters to parse.

    Raises:
        LetterIntegerParseError: Indicating general parse failure.

    Returns:
        Tuple[str, int] -- A tuple containing the first letter and
            following integer as its first and second items
            respectively.
    '''
    try:
        # First parse for letter and number;
        letter, number = validate_letter_and_float(chars_to_parse)
        # Convert float to int:
        integer = int(number)
    except (ValueError):
        raise ResponseValidationError('Unable to parse {} into a letter and integer.'.format(
            chars_to_parse))
    # Return values
    return (letter, integer)


def validate_letter_and_float(chars_to_parse: str) -> Tuple[str, float]:
    '''Parses a string whose first character is a letter, and
    whose following characters form a number, into a tuple
    containing a letter and a number.

    Args:
        chars_to_parse (str): Characters to parse.

    Raises:
        LetterFloatParseError: Indicating the string could not
            be parsed into the tuple.

    Returns:
        Tuple[str, float]: A tuple containing the first letter and
            following number as its first and second items respectively.
    '''
    # Catch empty string;
    if chars_to_parse == '' or len(chars_to_parse) < 1:
        raise ResponseValidationError('Unable to parse {} into a letter and decimal.'.format(
            chars_to_parse))
    # Check the first char is a letter;
    letter = chars_to_parse[0]
    if not letter.isalpha():
        raise ResponseValidationError('Unable to parse {} into a letter and decimal.'.format(
            chars_to_parse))
    # Check the remaining letters are numbers;
    number = chars_to_parse[1:]
    try:
        number = float(number)
    except ValueError:
        raise ResponseValidationError('Unable to parse {} into a letter and decimal.'.format(
            chars_to_parse))
    # Tests passed, so return the value;
    return (letter, number)
