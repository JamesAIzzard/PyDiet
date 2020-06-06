from typing import Tuple

from pyconsoleapp import PyConsoleAppException

class LetterIntegerParseError(PyConsoleAppException):
    pass

class NumberAndTextParseError(PyConsoleAppException):
    pass

def parse_number_and_text(qty_and_text: str) -> Tuple[float, str]:
    '''Parses a string made up of a number and text. Returns
    the two components seperately as a tuple, number first.

    Args:
        qty_and_text (str): String to parse.

    Raises:
        NumberAndTextParseError: If the string cannot be parsed
            into the two components.

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
        raise ValueError('Unable to parse {} into a number and text.'
                         .format(qty_and_text))
    # Return tuple;
    return output

def parse_letter_and_integer(chars_to_parse:str)-> Tuple[str, int]:
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
    # Catch empty string;
    if chars_to_parse == '' or len(chars_to_parse) < 1:
        raise LetterIntegerParseError
    # Check the first char is a letter;
    letter = chars_to_parse[0]
    if not letter.isalpha():
        raise LetterIntegerParseError
    # Check the remaining letters are numbers;
    integer = chars_to_parse[1:]
    try:
        integer = int(integer)
    except ValueError:
        raise LetterIntegerParseError
    # Tests passed, so return the value;
    return (letter, integer)