"""Tests for the HasSettableRecipeQuantities class."""
from unittest import TestCase

import model
from tests.persistence import fixtures as pfx


class TestConstructor(TestCase):
    """Tests for the constructor function."""

    def test_can_construct_simple_instance(self):
        """Check we can construct a simple instance."""
        self.assertTrue(model.recipes.HasSettableRecipeQuantities(), model.recipes.HasReadableRecipeQuantities)

    @pfx.use_test_database
    def test_can_construct_instance_with_data(self):
        """Check we can construct an instance with data, and check the data gets loaded."""
        data = {
            model.recipes.get_datafile_name_for_unique_value("Bread and Butter"): model.quantity.QuantityData(
                quantity_in_g=100,
                pref_unit='g'
            ),
            model.recipes.get_datafile_name_for_unique_value("Peanut Butter Toast"): model.quantity.QuantityData(
                quantity_in_g=200,
                pref_unit='g'
            )
        }

        # Create a test instance, passing in data.
        hsrq = model.recipes.HasSettableRecipeQuantities(recipe_quantities_data=data)

        # Check the data got loaded;
        self.assertEqual(data, hsrq.persistable_data)


class TestRecipeQuantitiesData(TestCase):
    """Tests for the recipe_quantities_data property."""

    @pfx.use_test_database
    def test_returns_correct_data(self):
        """Check we can construct an instance with data, and check the data gets loaded."""
        data = {
            model.recipes.get_datafile_name_for_unique_value("Bread and Butter"): model.quantity.QuantityData(
                quantity_in_g=100,
                pref_unit='g'
            ),
            model.recipes.get_datafile_name_for_unique_value("Peanut Butter Toast"): model.quantity.QuantityData(
                quantity_in_g=200,
                pref_unit='g'
            )
        }

        # Create a test instance, passing in data.
        hsrq = model.recipes.HasSettableRecipeQuantities(recipe_quantities_data=data)

        # Check the data got loaded;
        self.assertEqual(data, hsrq.recipe_quantities_data)
