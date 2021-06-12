"""Tests the RecipeBase class."""
from unittest import TestCase

from tests.model.recipes import fixtures as rfx


class TestUniqueValue(TestCase):
    """Tests the unique_value property."""

    def test_name_is_returned(self):
        """Checks that we get the recipe name back from the unique value field."""
        # Create a test instance;
        rb = rfx.RecipeBaseTestable(recipe_data=rfx.get_recipe_data(for_unique_name="Porridge"))

        # Check the property returns the name;
        self.assertEqual("Porridge", rb.unique_value)


class TestGetPathIntoDB(TestCase):
    """Checks the get_path_into_db property"""

    def test_correct_value_is_returned(self):
        """Check we get the correct value back from the method."""
        # Create a test instance;
        rb = rfx.RecipeBaseTestable(rfx.get_recipe_data())

        # Assert we get the right path back;
        self.assertEqual("C:/Users/james.izzard/Dropbox/pydiet/database/recipes", rb.get_path_into_db())


class TestPersistableData(TestCase):
    """Tests the persistable data property."""

    def test_correct_value_is_returned(self):
        """Checks the persistable data method returns the correct data."""
        # Grab some test data;
        data = rfx.get_recipe_data(for_unique_name="Porridge")

        # Create a test instance, passing in the data;
        rb = rfx.RecipeBaseTestable(recipe_data=data)

        # Assert we get the same data back from the persistable data property;
        self.assertEqual(
            data,
            rb.persistable_data
        )
