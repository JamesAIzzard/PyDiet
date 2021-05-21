"""Ingredient class tests."""
from unittest import TestCase

import model
import persistence
from tests import fixtures as tfx


class TestConstructor(TestCase):
    """Constructor method tests."""

    @tfx.use_test_database
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
