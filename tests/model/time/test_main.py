"""Tests for the time_str.main module."""
from unittest import TestCase

import model.time


class TestTimeIsInInterval(TestCase):
    """Tests for the time_is_in_interval function."""

    def test_returns_true_if_time_in_interval_and_interval_in_one_day(self):
        """Checks the function returns True if the time_str is within the interval
        and the start time_str is earlier than the end time_str (i.e on the same day)."""
        # Create an interval and target time_str;
        interval = "06:30-07:00"
        time = "06:45"

        # Check that we get true if was ask if the interval is within the specified time_str;
        self.assertTrue(model.time.time_is_in_interval(
            time_str=time,
            time_interval_str=interval
        ))

    def test_returns_true_if_time_in_interval_and_interval_spans_two_days(self):
        """Checks the function returns True if the time_str is within the interval
        and the start time_str is later than the end time_str (i.e on the previous day)."""
        # Create an interval spanning two days and target time_str;
        interval = "23:00-07:00"
        time = "06:45"

        # Check that we get true if was ask if the interval is within the specified time_str;
        self.assertTrue(model.time.time_is_in_interval(
            time_str=time,
            time_interval_str=interval
        ))

    def test_returns_false_if_time_is_outside_interval_and_interval_in_one_day(self):
        """Checks that the function returns false if the time_str is outside of the interval
        and the interval is contained in a single day."""
        # Create an interval and target time_str outside of that interval;
        interval = "06:30-07:00"
        time = "08:45"

        # Check that we get true if was ask if the interval is within the specified time_str;
        self.assertFalse(model.time.time_is_in_interval(
            time_str=time,
            time_interval_str=interval
        ))

    def test_returns_false_if_time_is_outside_interval_and_interval_spans_multiple_days(self):
        """Checks that the function returns false if the time_str is outside of the interval and the
        interval spans multiple days."""
        # Create an interval spanning two days and target time_str outside of that interval;
        interval = "23:00-07:00"
        time = "08:45"

        # Check that we get true if was ask if the interval is within the specified time_str;
        self.assertFalse(model.time.time_is_in_interval(
            time_str=time,
            time_interval_str=interval
        ))
