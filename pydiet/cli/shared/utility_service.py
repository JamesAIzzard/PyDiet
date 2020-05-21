from typing import List, Dict, Tuple

from pydiet.cli.shared.exceptions import LetterIntegerParseError

def create_number_name_map(list_to_map: List, start_num=1) -> Dict[int, str]:
    map: Dict[int, str] = {}
    for i, key in enumerate(list_to_map, start=start_num):
        map[i] = key
    return map

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
