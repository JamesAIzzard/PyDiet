"""Tests for the SettableRecipe class."""
from unittest import TestCase

import model
import persistence
from tests.model.recipes import fixtures as rfx


class TestConstructor(TestCase):
    """Tests the constructor function."""

    def test_can_construct_simple_instance(self):
        """Checks we can construct a simple instance."""
        self.assertTrue(
            isinstance(model.recipes.SettableRecipe(), model.recipes.SettableRecipe)
        )

    def test_loads_data_when_provided(self):
        """Checks any data provided gets loaded into the instance."""
        # Grab some data;
        data = rfx.get_recipe_data(for_unique_name="Porridge")

        # Create a test instance, passing data in;
        sr = model.recipes.SettableRecipe(recipe_data=data)

        # Assert the data was loaded;
        self.assertEqual(data, sr.persistable_data)

    def test_datafile_name_is_populated(self):
        """Checks the recipe datafile name gets populated."""
        # Grab the datafile name for a recipe;
        df_name = model.recipes.get_datafile_name_for_unique_value(unique_value="Porridge")

        # Create a test instance of that recipe;
        sr = model.recipes.SettableRecipe(recipe_data=rfx.get_recipe_data(for_unique_name="Porridge"))

        # Assert the datafile name is populated and correct;
        self.assertEqual(df_name, sr.datafile_name)


class TestName(TestCase):
    """Tests the name property."""

    def test_gets_name_correctly(self):
        """Checks the name is returned correctly."""
        # Create a test instance of a named recipe;
        sr = model.recipes.SettableRecipe(recipe_data=rfx.get_recipe_data(for_unique_name="Porridge"))

        # Assert we get that name back;
        self.assertEqual("Porridge", sr.name)

    def test_sets_available_name_correctly(self):
        """Checks that an available name can be set without error."""
        # Create an empty recipe instance;
        sr = model.recipes.SettableRecipe()

        # Assert the name is not defined;
        self.assertFalse(sr.name_is_defined)

        # Set the name;
        sr.name = "Test Recipe"

        # Assert the name was set correctly;
        self.assertTrue(sr.name_is_defined)
        self.assertEqual("Test Recipe", sr.name)

    def test_existing_name_can_be_changed_if_available(self):
        """Checks that an existing name can be overwritten if the name is available."""
        # Create a test instance of a named recipe;
        sr = model.recipes.SettableRecipe(recipe_data=rfx.get_recipe_data(for_unique_name="Porridge"))

        # Assert the name is as saved in the datafile;
        self.assertEqual("Porridge", sr.name)

        # Change the name;
        sr.name = "Test Recipe"

        # Assert the name was changed;
        self.assertEqual("Test Recipe", sr.name)

    def test_exception_if_name_already_taken(self):
        # Create an empty recipe instance;
        sr = model.recipes.SettableRecipe()

        # Assert the name is not defined;
        self.assertFalse(sr.name_is_defined)

        # Assert we get an exception if we set the name to something already taken;
        with self.assertRaises(persistence.exceptions.UniqueValueDuplicatedError):
            sr.name = "Porridge"


class TestLoadData(TestCase):
    """Tests for the load_data method."""

    def test_loads_data_correctly(self):
        """Checks that the method loads data correctly."""
        # Grab some test data;
        data = rfx.get_recipe_data(for_unique_name="Porridge")

        # Create an empty instance;
        sr = model.recipes.SettableRecipe()

        # Assert the data is empty;
        self.assertEqual(
            rfx.get_recipe_data(),
            sr.persistable_data
        )

        # Now load the data;
        sr.load_data(data=data)

        # Now assert the data is populated;
        self.assertEqual(
            data,
            sr.persistable_data
        )
