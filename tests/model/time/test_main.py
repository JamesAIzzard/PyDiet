"""Tests for the time.main module."""
from unittest import TestCase


class TestTimeIsInInterval(TestCase):
    """Tests for the time_is_in_interval function."""

    def test_returns_true_if_time_in_interval_and_interval_in_one_day(self):
        """Checks the function returns True if the time is within the interval
        and the start time is earlier than the end time (i.e on the same day)."""
        raise NotImplementedError

    def test_returns_true_if_time_in_interval_and_interval_spans_two_days(self):
        """Checks the function returns True if the time is within the interval
        and the start time is later than the end time (i.e on the previous day)."""
        raise NotImplementedError

    def test_returns_false_if_time_is_outside_interval_and_interval_in_one_day(self):
        """Checks that the function returns false if the time is outside of the interval
        and the interval is contained in a single day."""
        raise NotImplementedError

    def test_returns_false_if_time_is_outside_interval_and_interval_spans_multiple_days(self):
        """Checks that the function returns false if the time is outside of the interval and the
        interval spans multiple days."""
        raise NotImplementedError
