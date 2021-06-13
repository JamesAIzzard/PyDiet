"""Tests for the HasSettableInstructionSrc class."""
from unittest import TestCase

import model


class TestConstructor(TestCase):
    """Tests for the constructor function."""

    def test_can_create_a_simple_instance(self):
        """Checks we can create a simple instance."""
        self.assertTrue(isinstance(
            model.instructions.HasSettableInstructionSrc(),
            model.instructions.HasReadableInstructionSrc
        ))

    def test_data_is_loaded_if_provided(self):
        """Checks that any data provided to the constructor gets loaded
        onto the instance."""
        # Create some data;
        data = "www.instruction.com"

        # Create a test instance, passing in data;
        hsis = model.instructions.HasSettableInstructionSrc(
            instruction_src_data=data
        )

        # Check the data on the instance matches the data passed in;
        self.assertEqual(data, hsis.instruction_src)


class TestInstructionSrc(TestCase):
    """Tests for the instruction_src property."""

    def test_gets_value_correctly(self):
        """Test the property gets the value correctly."""
        # Create some data;
        data = "www.instruction.com"

        # Create a test instance, passing in data;
        hsis = model.instructions.HasSettableInstructionSrc(
            instruction_src_data=data
        )

        # Check the data on the instance matches the data passed in;
        self.assertEqual(data, hsis.instruction_src)

    def test_sets_value_correctly(self):
        """Test the property sets the value correctly."""
        # Create some test data;
        data = "www.instruction.com"

        # Create an empty test instance;
        hsis = model.instructions.HasSettableInstructionSrc()

        # Assert the instruction source is not defined;
        self.assertFalse(hsis.instruction_src_defined)

        # Set the data;
        hsis.instruction_src = data

        # Check the data was set;
        self.assertTrue(hsis.instruction_src_defined)
        self.assertEqual(data, hsis.instruction_src)


class TestLoadData(TestCase):
    """Tests for the load_data method."""

    def test_data_is_loaded_correctly(self):
        """Checks the method loads the data correctly."""
        # Create some test data;
        data = "www.instruction.com"

        # Create an empty test instance;
        hsis = model.instructions.HasSettableInstructionSrc()

        # Assert the instruction source is not defined;
        self.assertFalse(hsis.instruction_src_defined)

        # Load the data;
        hsis.load_data({'instruction_src': data})

        # Check the data was loaded correctly;
        self.assertTrue(hsis.instruction_src_defined)
        self.assertEqual(data, hsis.instruction_src)
