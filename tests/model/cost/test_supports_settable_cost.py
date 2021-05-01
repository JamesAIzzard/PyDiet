from unittest import TestCase

import model


class TestConstructor(TestCase):
    def test_correct_instance(self):
        self.assertTrue(model.cost.SupportsSettableCost(), model.cost.SupportsSettableCost)

    def test_loads_data(self):
        sc = model.cost.SupportsSettableCost(cost_data=model.cost.CostData(
            pref_unit='kg',
            ref_qty=120,
            cost_per_g=0.25
        ))
        self.assertEqual(sc._cost_data, model.cost.CostData(
            pref_unit='kg',
            ref_qty=120,
            cost_per_g=0.25
        ))


class TestCostPerG(TestCase):
    def test_sets_value_correctly(self):
        sc = model.cost.SupportsSettableCost()
        sc.cost_per_g = 0.025
        self.assertTrue(sc._cost_data['cost_per_g'] == 0.025)

    def test_unsets_correctly(self):
        sc = model.cost.SupportsSettableCost()
        sc.cost_per_g = None
        self.assertTrue(sc._cost_data['cost_per_g'] is None)

    def test_raises_exception_if_cost_invalid(self):
        sc = model.cost.SupportsSettableCost()
        with self.assertRaises(model.cost.exceptions.InvalidCostError):
            sc.cost_per_g = '-1'
        with self.assertRaises(model.cost.exceptions.InvalidCostError):
            sc.cost_per_g = 'hello'


class TestCostRefQty(TestCase):
    def test_sets_ref_qty_correctly(self):
        raise NotImplementedError


class TestSetCost(TestCase):
    def test_sets_cost_correctly(self):
        sc = model.cost.SupportsSettableCost()
        sc.set_cost(
            cost_gbp=12.50,
            qty=2,
            unit='kg'
        )
        self.assertEqual(sc.cost_per_g, 6.25 / 1000)
        self.assertEqual(sc.cost_pref_unit, 'kg')
        self.assertEqual(sc.cost_ref_qty, 2)
