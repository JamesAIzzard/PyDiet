
from unittest import TestCase
from typing import TYPE_CHECKING

from pinjector import inject

from pydiet.cli.shared.exceptions import LetterIntegerParseError

import dependencies

if TYPE_CHECKING:
    from pydiet.cli.shared import utility_service as cli_utility_service

class TestParseLetterAndInteger(TestCase):
    def setUp(self):
        self.cut:'cli_utility_service' = inject('pydiet.cli.utility_service')

    def test_parses_correctly(self):
        letter, integer = self.cut.parse_letter_and_integer('p1')
        self.assertEqual(letter, 'p')
        self.assertEqual(integer, 1)
        letter, integer = self.cut.parse_letter_and_integer('a12')
        self.assertEqual(letter, 'a')
        self.assertEqual(integer, 12)   
        letter, integer = self.cut.parse_letter_and_integer('a 12')
        self.assertEqual(letter, 'a')
        self.assertEqual(integer, 12)                         

    def test_catches_broken_string(self):
        with self.assertRaises(LetterIntegerParseError):
            self.cut.parse_letter_and_integer('')
        with self.assertRaises(LetterIntegerParseError):
            self.cut.parse_letter_and_integer('  ')  
        with self.assertRaises(LetterIntegerParseError):
            self.cut.parse_letter_and_integer('1')                                    
