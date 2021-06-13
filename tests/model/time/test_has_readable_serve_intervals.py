"""Tests for the HasReadableServeIntervals class."""
from unittest import TestCase

import model.time.exceptions
from tests.model.time import fixtures as tfx


class TestCanBeServedAt(TestCase):
    """Tests for the can_be_served_at method."""

    def test_returns_true_if_can_be_served_at_specified_time(self):
        """Checks the method returns true if the instance can be served at the specified time_str."""
        # Create a test instance with a couple of serve intervals;
        hrsi = tfx.HasReadableServeIntervalsTestable(serve_intervals_data=[
            "06:00-07:00",
            "10:50-14:00"
        ])

        # Assert we get True if we provide a time within one of those intervals;
        self.assertTrue(hrsi.can_be_served_at("06:30"))

    def test_returns_false_if_cannot_be_served_as_specified_time(self):
        """Checks the method returns false if the instance cannot be served at the specified time_str."""
        # Create a test instance with a couple of serve intervals;
        hrsi = tfx.HasReadableServeIntervalsTestable(serve_intervals_data=[
            "06:00-07:00",
            "10:50-14:00"
        ])

        # Assert we get True if we provide a time outside both of those intervals;
        self.assertFalse(hrsi.can_be_served_at("09:30"))

    def test_exception_if_time_is_invalid(self):
        """Checks we get the right exception if we pass an invalid time."""
        # Create a test instance with a couple of serve intervals;
        hrsi = tfx.HasReadableServeIntervalsTestable(serve_intervals_data=[
            "06:00-07:00",
            "10:50-14:00"
        ])

        # Test we get an exception if we pass an invalid time;
        with self.assertRaises(model.time.exceptions.TimeValueError):
            _ = hrsi.can_be_served_at("25:00")


class TestPersistableData(TestCase):
    """Tests for the persistable data property."""

    def test_correct_data_is_returned(self):
        """Tests the data is returned correctly."""
        # Create some test data;
        si_data = [
            "06:00-10:00",
            "11:00-14:00"
        ]

        # Create a test instance, passing this data in;
        hrsi = tfx.HasReadableServeIntervalsTestable(serve_intervals_data=si_data)

        # Assert we get this data back;
        self.assertEqual(
            si_data, hrsi.persistable_data['serve_intervals']
        )
