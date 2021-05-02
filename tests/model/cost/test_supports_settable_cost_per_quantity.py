from unittest import TestCase

import model


class TestConstructor(TestCase):
    def test_correct_instance(self):
        self.assertTrue(model.cost.SupportsSettableCostPerQuantity(), model.cost.SupportsSettableCostPerQuantity)

    def test_loads_data(self):
        sc = model.cost.SupportsSettableCostPerQuantity(cost_data=model.cost.CostPerQtyData(
            pref_unit='kg',
            ref_qty=120,
            cost_per_g=0.25
        ))
        self.assertEqual(sc._cost_per_qty_data, model.cost.CostPerQtyData(
            pref_unit='kg',
            ref_qty=120,
            cost_per_g=0.25
        ))


class TestCostPerG(TestCase):
    def test_sets_value_correctly(self):
        sc = model.cost.SupportsSettableCostPerQuantity()
        sc.cost_per_g = 0.025
        self.assertTrue(sc._cost_per_qty_data['cost_per_g'] == 0.025)

    def test_unsets_correctly(self):
        sc = model.cost.SupportsSettableCostPerQuantity()
        sc.cost_per_g = None
        self.assertTrue(sc._cost_per_qty_data['cost_per_g'] is None)

    def test_raises_exception_if_cost_invalid(self):
        sc = model.cost.SupportsSettableCostPerQuantity()
        with self.assertRaises(model.cost.exceptions.InvalidCostError):
            sc.cost_per_g = '-1'
        with self.assertRaises(model.cost.exceptions.InvalidCostError):
            sc.cost_per_g = 'hello'


class TestCostRefQty(TestCase):
    def test_sets_ref_qty_correctly(self):
        sc = model.cost.SupportsSettableCostPerQuantity()
        sc.cost_ref_qty = 122
        self.assertTrue(sc._cost_per_qty_data['ref_qty'] == 122)

    def test_raises_exception_if_qty_zero(self):
        sc = model.cost.SupportsSettableCostPerQuantity()
        with self.assertRaises(model.cost.exceptions.InvalidCostError):
            sc.cost_ref_qty = 0

    def test_raises_exception_if_qty_invalid(self):
        sc = model.cost.SupportsSettableCostPerQuantity()
        with self.assertRaises(model.cost.exceptions.InvalidCostError):
            sc.cost_ref_qty = "hello"
        with self.assertRaises(model.cost.exceptions.InvalidCostError):
            sc.cost_ref_qty = -1

class TestSetCost(TestCase):
    def test_sets_cost_correctly(self):
        sc = model.cost.SupportsSettableCostPerQuantity()
        sc.set_cost(
            cost_gbp=12.50,
            qty=2,
            unit='kg'
        )
        self.assertEqual(sc.cost_per_g, 6.25 / 1000)
        self.assertEqual(sc.cost_pref_unit, 'kg')
        self.assertEqual(sc.cost_ref_qty, 2)
