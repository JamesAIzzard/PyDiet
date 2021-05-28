"""Tests for the SettableIngredient class."""
from unittest import TestCase

import model
import persistence
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
            for_unique_name=fx.get_ingredient_name_with("typical_fully_defined_data")
        ))

        # Load the test data directly;
        data = fx.get_ingredient_data(for_unique_name=fx.get_ingredient_name_with("typical_fully_defined_data"))

        # Check the test data matches the ingredient's persistable data;
        self.assertEqual(data, si.persistable_data)


class TestMissingMandatoryAttrs(TestCase):
    """Checks the mandatory attributes which can only be undefined on the settable variant of Ingredient."""

    @pfx.use_test_database
    def test_name_is_listed_when_undefined(self):
        """Checks we get the mandatory attributes listed if any are undefined."""
        # Create an empty test instance;
        si = model.ingredients.SettableIngredient()

        # Assert that 'name' is in the missing attribtues list when undefined;
        self.assertTrue('name' in si.missing_mandatory_attrs)

    @pfx.use_test_database
    def test_cost_is_listed_when_undefined(self):
        """Checks cost is in undefined list when cost is undefined."""
        # Load the test instance;
        si = model.ingredients.SettableIngredient(ingredient_data=fx.get_ingredient_data(
            for_unique_name=fx.get_ingredient_name_with("cost_per_g_undefined")
        ))

        # Check the cost is in the undefined list;
        self.assertTrue('cost' in si.missing_mandatory_attrs)

    @pfx.use_test_database
    def test_defining_cost_removes_cost_from_list(self):
        """Checks we can remove cost from the missing attributes list by defining it."""
        # Load the test instance;
        si = model.ingredients.SettableIngredient(ingredient_data=fx.get_ingredient_data(
            for_unique_name=fx.get_ingredient_name_with("cost_per_g_undefined")
        ))

        # Check the cost is in the undefined list;
        self.assertTrue('cost' in si.missing_mandatory_attrs)

        # Now define cost;
        si.set_cost(
            cost_gbp=12.00,
            qty=3,
            unit='kg'
        )

        # Now assert cost is no longer on the list;
        self.assertFalse('cost' in si.missing_mandatory_attrs)


class TestsName(TestCase):
    """Tests the name property."""

    @pfx.use_test_database
    def test_unique_name_can_be_set(self):
        """Tests the name property can be used to set a name which is not already in use in the database."""
        # Create a fresh test instance;
        si: 'model.HasSettableName' = model.ingredients.SettableIngredient()

        # Assert the name is not set;
        with self.assertRaises(model.exceptions.UndefinedNameError):
            _ = si.name

        # Set the name
        si.name = "Made Up Ingredient"

        # Assert that the name was set;
        self.assertEqual("Made Up Ingredient", si.name)

    @pfx.use_test_database
    def test_exception_if_name_already_in_use(self):
        """Tests that we get an exception if we try to set a name that is already in use in the database."""
        # Create a fresh test instance;
        si: 'model.HasSettableName' = model.ingredients.SettableIngredient()

        # Assert the name is not set;
        with self.assertRaises(model.exceptions.UndefinedNameError):
            _ = si.name

        # Assert we get an exception if we try to set a name that is already in use;
        with self.assertRaises(persistence.exceptions.UniqueValueDuplicatedError):
            si.name = "Lemon"
