"""Tests for the HasSettableName class."""
from unittest import TestCase

import model


class TestLoadData(TestCase):
    """Tests the load data method."""

    def test_loads_name_correctly(self):
        """Test that a name is loaded onto the instance correctly."""
        # Create some test data;
        name = "Mock Name"

        # Create a test instance;
        hsn = model.HasSettableName()

        # Assert the name is not yet defined;
        self.assertFalse(hsn.name_is_defined)

        # Now load the name;
        hsn.load_data(data={'name': name})

        # Now assert the name is populated;
        self.assertTrue(hsn.name_is_defined)
        self.assertEqual(name, hsn.name)

    def test_no_exception_if_name_key_not_in_data_dict(self):
        """Checks that we don't get an exception if there is no name key in the data dict."""
        # Create a test instance;
        hsn = model.HasSettableName()

        # Load some empty data;
        hsn.load_data(data={})

        # Assert the name is still empty;
        self.assertFalse(hsn.name_is_defined)
