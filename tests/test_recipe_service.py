from unittest import TestCase

from pydiet.recipes import recipe_service as rs
from pydiet.recipes.exceptions import (
    TimeIntervalValueError,
    TimeIntervalParseError
)

class TestParseTimeInterval(TestCase):

    def test_parses_correctly(self):
        output = rs.parse_time_interval("06:00-10:00")
        self.assertEqual(output, "06:00-10:00")
    
    def test_corrects_single_digits(self):
        output = rs.parse_time_interval("6:00-10:00")
        self.assertEqual(output, "06:00-10:00")
        output = rs.parse_time_interval("11:00-9:5")
        self.assertEqual(output, "11:00-09:05")    

    def test_catches_impossible_times(self):
        with self.assertRaises(TimeIntervalValueError):
            rs.parse_time_interval("60:00-10:00")
        with self.assertRaises(TimeIntervalValueError):
            rs.parse_time_interval("9:00-25:00")

    def test_catches_one_ended_intervals(self):
        with self.assertRaises(TimeIntervalParseError):
            rs.parse_time_interval("11:00")

    def test_catches_nonsense_string_input(self):
        with self.assertRaises(TimeIntervalParseError):
            rs.parse_time_interval("alsdkjdagf")

    def test_catches_identical_time_endpoints(self):
        with self.assertRaises(TimeIntervalValueError):
            rs.parse_time_interval("9:00-9:00")





