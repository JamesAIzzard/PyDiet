"""Tests for the ReadableRecipe class."""
from unittest import TestCase

import model
from tests.model.recipes import fixtures as rfx


class TestConstructor(TestCase):
    """Tests the constructor function."""

    def test_can_construct_simple_instance(self):
        """Checks we can construct a simple instance."""
        self.assertTrue(isinstance(
            model.recipes.ReadonlyRecipe(recipe_data_src=lambda: rfx.get_recipe_data()),
            model.recipes.ReadonlyRecipe
        ))

    def test_data_is_loaded_correctly(self):
        """Checks any data that is passed in gets loaded correctly."""
        # Create some test data;
        rd = rfx.get_recipe_data(for_unique_name="Porridge")

        # Create a test instance, passing in some data;
        rr = model.recipes.ReadonlyRecipe(recipe_data_src=lambda: rd)

        # Assert that the persistable data is the same data that we passed in;
        self.assertEqual(rd, rr.persistable_data)
