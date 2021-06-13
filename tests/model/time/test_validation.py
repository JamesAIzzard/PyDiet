"""Tests for the time_str.validation module."""
from unittest import TestCase

import model


class TestValidateTime(TestCase):
    """Tests for the validate_time function."""

    def test_valid_time_passes(self):
        """Checks that a vlaid time_str passes validation."""
        # Define a valid time_str;
        valid_time = "06:00"

        # Assert we get no exception if we pass it in
        self.assertEqual(
            valid_time,
            model.time.validation.validate_time(valid_time)
        )

    def test_totally_invalid_string_raises_exception(self):
        """Checks that a totally invalid string raises the correct exception."""
        # Define an invalid time_str string;
        invalid_time = "invalid"

        # Assert we get an exception if we validate it;
        with self.assertRaises(model.time.exceptions.TimeValueError):
            model.time.validation.validate_time(invalid_time)

    def test_time_greater_than_24h_raises_exception(self):
        """Checks that we get the correct exception if the time_str is greater than 24H."""
        # Define a time_str which is greater than 24h;
        invalid_time = "25:00"

        # Assert we get an exception if we validate it;
        with self.assertRaises(model.time.exceptions.TimeValueError):
            model.time.validation.validate_time(invalid_time)


class TestValidateTimeInterval(TestCase):
    """Tests for the validate_time_interval function."""

    def test_valid_interval_passes(self):
        """Checks that a valid time_str interval does not raise an exception."""
        # Define a valid interval;
        valid_interval = "06:00-10:00"

        # Assert we get no exception;
        _ = model.time.validation.validate_time_interval(valid_interval)

    def test_totally_invalid_string_raises_exception(self):
        """Checks that a totally invalid string raises the correct exception."""
        # Define a totally invalid string;
        invalid_interval = "invalid"

        # Assert we get an exception when we try to validate it;
        with self.assertRaises(model.time.exceptions.TimeIntervalValueError):
            _ = model.time.validation.validate_time_interval(invalid_interval)

    def test_single_time_with_sep_raises_exception(self):
        """Checks we get an exception if we pass in only the start time_str with the sperator hyphen."""
        # Define a string which only contains a single time_str;
        invalid_interval = "06:00-"

        # Assert we get an exception when we try to validate it;
        with self.assertRaises(model.time.exceptions.TimeValueError):
            _ = model.time.validation.validate_time_interval(invalid_interval)

    def test_single_time_with_no_sep_raises_exception(self):
        """Checks we get an exception if we pass in only half of the interval."""
        # Define a string which only contains a single time_str;
        invalid_interval = "06:00"

        # Assert we get an exception when we try to validate it;
        with self.assertRaises(model.time.exceptions.TimeIntervalValueError):
            _ = model.time.validation.validate_time_interval(invalid_interval)

    def test_three_time_parts_raise_exception(self):
        """Checks we get an exception if we pass in three time_str parts."""
        # Define a string which contains three time_str components;
        invalid_interval = "06:00-12:00-14:00"

        # Assert we get an exception when we try to validate it;
        with self.assertRaises(model.time.exceptions.TimeIntervalValueError):
            _ = model.time.validation.validate_time_interval(invalid_interval)

    def test_exception_if_interval_has_no_length(self):
        """Checks that we get an exception if the interval has no length;"""
        # Define an interval string where the start time and end time are the same;
        interval = "07:45-07:45"

        # Assert we get an exception if we try to validate it;
        with self.assertRaises(model.time.exceptions.TimeIntervalValueError):
            _ = model.time.validation.validate_time_interval(interval)
