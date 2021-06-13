"""Tests for HasReadableInstructionSrc class."""
from unittest import TestCase

from tests.model.instructions import fixtures as infx


class TestInstructionSrcDefined(TestCase):
    """Tests the instruction_src_defined property."""

    def test_returns_true_if_src_defined(self):
        """Checks the property returns True if the instruction src is defined."""
        # Create a test instance, passing in data;
        hris = infx.HasReadableInstructionSrcTestable(instruction_src="www.instruction.com")

        # Assert the src is defined;
        self.assertTrue(hris.instruction_src_defined)

    def test_returns_false_if_src_undefined(self):
        """Checks the property returns False if the instruction src is undefined."""
        # Create an empty test instance;
        hris = infx.HasReadableInstructionSrcTestable()

        # Assert the src is defined;
        self.assertFalse(hris.instruction_src_defined)


class TestPersistableData(TestCase):
    """Tests the persistable_data property."""

    def test_data_is_correct(self):
        """Check that the persistable data is returned correctly."""
        # Create a test instance;
        hris = infx.HasReadableInstructionSrcTestable(instruction_src="www.instruction.com")

        # Check we get the instruction out in the persistable data;
        self.assertEqual(
            "www.instruction.com",
            hris.persistable_data['instruction_src']
        )
