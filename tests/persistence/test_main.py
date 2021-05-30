"""Tests for functionality in persistence.main"""
from unittest import TestCase

import model
import persistence
from tests.persistence import fixtures as fx


class TestGetDatafileNameForUniqueValue(TestCase):
    """Tests for get_datafile_name_for_unique_value method."""

    @fx.use_test_database
    def test_gets_correct_df_name(self):
        """Check that the correct datafile name is returned."""
        # Assert we get the df name we are expecting;
        self.assertEqual(
            "1198a703-ae23-4303-9b21-dd8ef9d16548",
            persistence.get_datafile_name_for_unique_value(
                cls=model.ingredients.Ingredient,
                unique_value="Honey"
            )
        )

    @fx.use_test_database
    def test_raises_exception_if_name_not_found(self):
        """Check that we get an exception if we don't recognise the unique name."""
        # Check we see the exception;
        with self.assertRaises(persistence.exceptions.UniqueValueNotFoundError):
            _ = persistence.get_datafile_name_for_unique_value(
                cls=model.ingredients.Ingredient,
                unique_value="fake"
            )
