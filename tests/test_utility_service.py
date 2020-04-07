import sys
# sys.path.append('/home/james/Documents/PyDiet') # Ubuntu Desktop
# sys.path.append('c:\\Users\\james.izzard\\Documents\\PyDiet') # Work Laptop
sys.path.append('C:\\Users\\James.Izzard\\Documents\\PyDiet') # Work Desktop

from unittest import TestCase
from typing import TYPE_CHECKING

from pinjector import inject

import dependencies

if TYPE_CHECKING:
    from pydiet import utility_service

class TestUtilityService(TestCase):
    def setUp(self):
        self.ut:'utility_service' = inject('pydiet.utility_service')

    def test_score_similarity(self):
        words = ["one", "two", "three", "four"]
        search_term = "one"
        score = self.ut.score_similarity(words, search_term)
        self.assertEqual(score["one"], 1.0)