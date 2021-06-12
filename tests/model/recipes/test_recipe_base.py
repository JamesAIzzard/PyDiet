"""Tests the RecipeBase class."""
from unittest import TestCase

from tests.model.recipes import fixtures as rfx


class TestGetPathIntoDB(TestCase):
    """Checks the get_path_into_db property"""

    def test_correct_value_is_returned(self):
        """Check we get the correct value back from the method."""
        # Create a test instance;
        rb = rfx.RecipeBaseTestable(rfx.get_recipe_data())

        # Assert we get the right path back;
        self.assertEqual("C:/Users/james.izzard/Dropbox/pydiet/database/recipes", rb.get_path_into_db())
