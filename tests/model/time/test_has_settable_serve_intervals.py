"""Tests for the HasSettableServeIntervals class."""
from unittest import TestCase

import model


class TestConstructor(TestCase):
    """Tests the constructor function."""

    def test_can_construct_simple_instance(self):
        """Checks that we can construct a simple instance."""
        hssi = model.time.HasSettableServeIntervals()
        self.assertTrue(hssi, model.time.HasSettableServeIntervals)

    def test_loads_data_when_provided(self):
        """Checks that the constructor loads serve interval data into the instance when
        it is provided."""
        # Define some load intervals data;
        data = [
            "06:00-07:30",
            "10:00-13:00"
        ]

        # Pass this data in when we create a test instance;
        hssi = model.time.HasSettableServeIntervals(serve_times_data=data)

        # Check that the data we get out matches the data we put in;
        self.assertEqual(
            data,
            hssi.serve_intervals_data
        )

    def test_raises_exception_if_data_provided_is_invalid(self):
        """Checks that an exception is raised if the data provided is invalid."""
        # Define some load intervals data, with an invalid row;
        data = [
            "06:00-07:30",
            "invalid"
        ]

        # Check we get an exception when we try to create the test instance;
        with self.assertRaises(model.time.exceptions.TimeIntervalValueError):
            hssi = model.time.HasSettableServeIntervals(serve_times_data=data)


class TestServeIntervalsData(TestCase):
    """Tests the serve_intervals_data property."""

    def test_returns_correct_data(self):
        """Checks that the method returns the correct data."""
        # Define some load intervals data;
        data = [
            "06:00-07:30",
            "10:00-13:00"
        ]

        # Pass this data in when we create a test instance;
        hssi = model.time.HasSettableServeIntervals(serve_times_data=data)

        # Check that the data we get out matches the data we put in;
        self.assertEqual(
            data,
            hssi.serve_intervals_data
        )


class TestAddServeInterval(TestCase):
    """Tests the add_serve_interval method."""

    def test_can_add_serve_interval(self):
        """Checks that we can add a serve interval."""
        # Create a test instance;
        hssi = model.time.HasSettableServeIntervals()

        # Assert there are no intervals yet;
        self.assertEqual([], hssi.serve_intervals_data)

        # Add an interval;
        hssi.add_serve_interval("06:00-07:00")

        # Assert this interval has been added;
        self.assertEqual(["06:00-07:00"], hssi.serve_intervals_data)

    def test_exception_if_serve_interval_invalid(self):
        """Checks we get an exception if the serve interval is invalid."""
        # Create a test instance;
        hssi = model.time.HasSettableServeIntervals()

        # Check we get an exception if we try to fork in invalid data;
        with self.assertRaises(model.time.exceptions.TimeIntervalValueError):
            hssi.add_serve_interval("invalid")


class TestLoadData(TestCase):
    """Tests the load_data method."""

    def test_loads_data_correctly(self):
        """Checks that the data is loaded correctly."""
        # Define some load intervals data;
        data = [
            "06:00-07:30",
            "10:00-13:00"
        ]

        # Pass this data in when we create a test instance;
        hssi = model.time.HasSettableServeIntervals(serve_times_data=data)

        # Check that the data we get out matches the data we put in;
        self.assertEqual(
            data,
            hssi.persistable_data['serve_intervals']
        )
