"""Tests for the SettableIngredient class."""
from unittest import TestCase

import model
import persistence
from tests.model.ingredients import fixtures as fx
from tests.model.quantity import fixtures as qfx
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


class TestName(TestCase):
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
    def test_name_can_be_set_to_none(self):
        """Checks the name can be set to None without an exception."""
        # Create a test instance, providing data;
        si = model.ingredients.SettableIngredient(ingredient_data=fx.get_ingredient_data(
            for_unique_name=fx.get_ingredient_name_with("typical_fully_defined_data")
        ))

        # Assert the name is set;
        self.assertTrue(si.name_is_defined)

        # Set the name to None;
        si.name = None

        # Assert that the name is no longer set;
        self.assertFalse(si.name_is_defined)
        self.assertTrue("name" in si.missing_mandatory_attrs)

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


class TestSetCost(TestCase):
    """Tests the set cost method."""

    def test_valid_cost_can_be_set(self):
        """Checks a valid cost can be set."""
        # Create a fresh test instance;
        si = model.ingredients.SettableIngredient()

        # Assert the cost is not defined;
        self.assertFalse(si.cost_is_defined)

        # Set the cost;
        si.set_cost(
            cost_gbp=12.50,
            qty=3.5,
            unit="kg"
        )

        # Assert the cost has been set;
        self.assertTrue(si.cost_is_defined)
        self.assertEqual(12.5, si.cost_of_ref_qty)
        self.assertEqual("kg", si.cost_ref_subject_quantity.pref_unit)
        self.assertEqual(3.5, si.cost_ref_subject_quantity.ref_qty)

    def test_exception_if_cost_value_invalid(self):
        """Checks we get an exception if the cost being set is invalid."""
        # Create a fresh test instance;
        si = model.ingredients.SettableIngredient()

        # Check we get an exception if the cost value is invalid;
        with self.assertRaises(model.cost.exceptions.InvalidCostError):
            si.set_cost(
                cost_gbp="invalid", # noqa
                qty=3.5,
                unit="kg"
            )

    def test_exception_if_ref_qty_zero(self):
        """Checks we get an exception if the reference quantity the cost is being set against is zero."""
        # Create a fresh test instance;
        si = model.ingredients.SettableIngredient()

        # Check we get an exception if the cost ref qty is zero;
        with self.assertRaises(model.quantity.exceptions.ZeroQtyError):
            si.set_cost(
                cost_gbp=2.50,
                qty=0,
                unit="kg"
            )

    def test_can_use_ext_units_if_configured(self):
        """Checks that we can set the cost against an extended unit if the correct units are configured."""
        # Create a fresh test instance, with extended units configured;
        si = model.ingredients.SettableIngredient(
            ingredient_data={
                'extended_units_data': qfx.get_extended_units_data(g_per_ml=1.2)
            }
        )

        # Assert the cost is not defined;
        self.assertFalse(si.cost_is_defined)

        # Assert we can set the cost against an extended unit;
        si.set_cost(
            cost_gbp=2.50,
            qty=1.5,
            unit="L"
        )

        # Assert the cost has now been set;
        self.assertTrue(si.cost_is_defined)

    def test_exception_if_ext_units_when_not_configured(self):
        """Checks we get an exception if we try to use extended units to define the cost,
        when extended units are not configured."""
        raise NotImplementedError
