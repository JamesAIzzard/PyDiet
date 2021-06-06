"""Tests for SupportsSettableCostPerQuantity class."""
from unittest import TestCase

import model
from tests.model.cost import fixtures as fx


class TestConstructor(TestCase):
    """Tests for the constructor."""

    def test_correct_instance(self):
        """Checks we can create a simple instance."""
        # Check a simple instance is created OK.
        self.assertTrue(model.cost.HasSettableCostPerQuantity(), model.cost.HasSettableCostPerQuantity)

    def test_loads_data(self):
        """Check any data we pass in gets loaded."""
        # Create some test data;
        data = model.cost.CostPerQtyData(
            pref_unit='kg',
            quantity_in_g=1200,
            cost_per_g=0.25
        )

        # Create a test instance, passing in data;
        sc = model.cost.HasSettableCostPerQuantity(cost_per_qty_data=data)

        # Check the correct data shows up;
        self.assertEqual(data, sc.cost_per_qty_data)


class TestSubjectQuantity(TestCase):
    def test_subject_quantity_is_settable(self):
        sc = model.cost.HasSettableCostPerQuantity()
        self.assertTrue(isinstance(sc.cost_ref_subject_quantity, model.quantity.IsSettableQuantityOf))


class TestSetCost(TestCase):
    def test_sets_cost_correctly(self):
        sc = model.cost.HasSettableCostPerQuantity()
        sc.set_cost(
            cost_gbp=12.50,
            qty=2,
            unit='kg'
        )
        self.assertEqual(sc.cost_per_g, 6.25 / 1000)
        self.assertEqual(sc.cost_ref_subject_quantity.qty_pref_unit, 'kg')
        self.assertEqual(sc.cost_ref_subject_quantity.ref_qty, 2)

    def test_unsets_correctly(self):
        sc = model.cost.HasSettableCostPerQuantity(cost_per_qty_data=model.cost.CostPerQtyData(
            pref_unit='kg',
            quantity_in_g=1200,
            cost_per_g=0.25
        ))
        sc.set_cost(cost_gbp=None)
        self.assertEqual(sc._cost_per_g_, None)


class TestLoadData(TestCase):
    """Tests the load data method."""
    def test_data_is_loaded_correctly(self):
        """Checks the method loads valid data correctly."""
        # Create some data to test with;
        data = fx.get_cost_per_qty_data(
            cost_per_g=0.02,
            quantity_in_g=200,
            pref_unit='lb'
        )

        # Create a test instance;
        sc = model.cost.HasSettableCostPerQuantity()

        # Check the cost is not defined;
        self.assertFalse(sc.cost_is_defined)

        # Now pass the data in to load;
        sc.load_data(data={'cost_per_qty_data': data})

        # Now check the data was loaded correctly;
        self.assertTrue(sc.cost_is_defined)
        self.assertEqual(0.02, sc.cost_per_g)
        self.assertEqual(200, sc.cost_ref_subject_quantity.quantity_in_g)
        self.assertEqual('lb', sc.cost_ref_subject_quantity.qty_pref_unit)

    def test_no_exception_if_data_not_present(self):
        """Checks the load method does not fail if there is no cost data in the data dict."""
        # Create a fresh instance;
        sc = model.cost.HasSettableCostPerQuantity()

        # Try and load an empty data dict;
        sc.load_data(data={})

        # Assert data is still empty;
        self.assertFalse(sc.cost_is_defined)


