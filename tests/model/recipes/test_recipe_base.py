"""Tests the RecipeBase class."""
from unittest import TestCase

import model
from tests.model.recipes import fixtures as rfx


class TestName(TestCase):
    """Tests the name property."""

    def test_name_is_correct(self):
        """Test the name property returns the correct value."""
        # Create a named test instance;
        rb = rfx.RecipeBaseTestable()

        # Check the name is correct;
        self.assertEqual("Porridge")
