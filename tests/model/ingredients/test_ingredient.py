"""Ingredient class tests."""
from unittest import TestCase

import model
import persistence
from tests.persistence import fixtures as pfx


class TestConstructor(TestCase):
    """Constructor method tests."""

    @pfx.use_test_database
    def test_can_create_instance_from_unique_name(self):
        """Check we can initialise an instance from the unique name."""
        # First, create the instance;
        i_name = "Honey"
        i = model.ingredients.Ingredient(unique_name=i_name)

        # Now load the instance's data directly;
        fp = "{path_into_db}/{df_name}.json".format(
            path_into_db=model.ingredients.Ingredient.get_path_into_db(),
            df_name=persistence.main.get_datafile_name_for_unique_value(
                cls=model.ingredients.Ingredient,
                unique_value=i_name
            )
        )
        data = persistence.main._read_datafile(filepath=fp)

        # Check that the instance data matches the data in the database;
        self.assertEqual(data, i.persistable_data)

    @pfx.use_test_database
    def test_can_create_instance_from_datafile_name(self):
        """Check we can initialise the ingredient from the datafile name."""
        # First, create the instance;
        df_name = "1198a703-ae23-4303-9b21-dd8ef9d16548"
        i = model.ingredients.Ingredient(datafile_name=df_name)

        # Now load the instance's data directly;
        fp = "{path_into_db}/{df_name}.json".format(
            path_into_db=model.ingredients.Ingredient.get_path_into_db(),
            df_name=df_name
            )
        data = persistence.main._read_datafile(filepath=fp)

        # Check that the instance data matches the data in the database;
        self.assertEqual(data, i.persistable_data)

    @pfx.use_test_database
    def test_raises_exception_if_no_name_provided(self):
        """Check we get an exception if we try and initialise an ingredient without providing a name."""
        with self.assertRaises(ValueError):
            _ = model.ingredients.Ingredient()
