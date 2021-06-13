"""Tests for the HasReadableServeIntervals class."""
from unittest import TestCase

from tests.model.time import fixtures as tfx


class TestCanBeServedAt(TestCase):
    """Tests for the can_be_served_at method."""

    def returns_true_if_can_be_served_at_specified_time(self):
        """Checks the method returns true if the instance can be served at the specified time_str."""
        raise NotImplementedError

    def returns_false_if_cannot_be_served_as_specified_time(self):
        """Checks the method returns false if the instance cannot be served at the specified time_str."""
        raise NotImplementedError


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
