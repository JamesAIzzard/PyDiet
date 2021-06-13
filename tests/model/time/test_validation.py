"""Tests for the time.validation module."""
from unittest import TestCase

import model


class TestValidateTime(TestCase):
    """Tests for the validate_time function."""

    def test_valid_time_passes(self):
        """Checks that a vlaid time passes validation."""
        # Define a valid time;
        valid_time = "06:00"

        # Assert we get no exception if we pass it in
        self.assertEqual(
            valid_time,
            model.time.validate_time(valid_time)
        )

    def test_totally_invalid_string_raises_exception(self):
        """Checks that a totally invalid string raises the correct exception."""
        # Define an invalid time string;
        invalid_time = "invalid"

        # Assert we get an exception if we validate it;
        with self.assertRaises(model.time.exceptions.TimeValueError):
            model.time.validate_time(invalid_time)

    def test_time_greater_than_24h_raises_exception(self):
        """Checks that we get the correct exception if the time is greater than 24H."""
        # Define a time which is greater than 24h;
        invalid_time = "25:00"

        # Assert we get an exception if we validate it;
        with self.assertRaises(model.time.exceptions.TimeValueError):
            model.time.validate_time(invalid_time)


class TestValidateTimeInterval(TestCase):
    """Tests for the validate_time_interval function."""

    def test_valid_interval_passes(self):
        """Checks that a valid time interval does not raise an exception."""
        raise NotImplementedError

    def test_totally_invalid_string_raises_exception(self):
        """Checks that a totally invalid string raises the correct exception."""
        raise NotImplementedError

    def test_single_time_raises_exception(self):
        """Checks we get an exception if we pass in only half of the interval."""
        raise NotImplementedError

    def test_three_time_parts_raise_exception(self):
        """Checks we get an exception if we pass in three time parts."""
        raise NotImplementedError
