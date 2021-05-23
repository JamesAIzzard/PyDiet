"""Tests for the SettableIngredient class."""
from unittest import TestCase

import model
from tests.model.ingredients import fixtures as fx
from tests.persistence import fixtures as pfx


class TestConstructor(TestCase):
    """Tests the SettableIngredient constructor functionality."""

    def test_can_construct_an_instance_without_providing_data(self):
        """Check that we don't need to pass data in to construct an instance."""
        self.assertTrue(isinstance(
            model.ingredients.SettableIngredient(),
            model.ingredients.SettableIngredient
        ))

    @pfx.use_test_database
    def test_loads_data_if_provided(self):
        """Checks that the instance loads data if it is provided."""
        # Create a test instance, providing data;
        si = model.ingredients.SettableIngredient(ingredient_data=fx.get_ingredient_data(
            for_unique_name=fx.get_ingredient_name_with("typical_data")
        ))

        # Load the test data directly;
        data = fx.get_ingredient_data(for_unique_name=fx.get_ingredient_name_with("typical_data"))

        # Check the test data matches the ingredient's persistable data;
        self.assertEqual(data, si.persistable_data)
