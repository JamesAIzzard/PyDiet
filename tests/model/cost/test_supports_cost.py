from unittest import TestCase

import model
from tests.model.cost import fixtures as fx


class TestCostPerG(TestCase):
    def test_result_is_correct(self):
        sc = fx.SupportsCostTestable(cost_per_g=0.25)
        self.assertEqual(sc.cost_per_g, 0.25)

    def test_raises_exception_if_undefined(self):
        sc = fx.SupportsCostTestable()
        with self.assertRaises(model.cost.exceptions.UndefinedCostError):
            _ = sc.cost_per_g


class TestCostPrefUnit(TestCase):
    def test_correct_unit_returned(self):
        sc = fx.SupportsCostTestable(pref_unit='kg')
        self.assertTrue(sc.cost_pref_unit == 'kg')

    def test_falls_back_if_unit_not_configured(self):
        sc = fx.SupportsCostTestable(pref_unit='L')
        self.assertTrue(sc.cost_pref_unit == 'g')


class TestCostRefQty(TestCase):
    def test_correct_qty_returned(self):
        sc = fx.SupportsCostTestable(ref_qty=12)
        self.assertTrue(sc.cost_ref_qty == 12)

    def test_falls_back_if_unit_not_configured(self):
        sc = fx.SupportsCostTestable(pref_unit='L', ref_qty=1.2)
        self.assertTrue(sc.cost_ref_qty == 100)


class TestCostPerPrefUnit(TestCase):
    def test_result_is_correct(self):
        sc = fx.SupportsCostTestable(pref_unit='kg', cost_per_g=0.5)
        self.assertEqual(sc.cost_per_pref_unit, 500)


class TestCostOfRefQty(TestCase):
    def test_result_is_correct(self):
        sc = fx.SupportsCostTestable(pref_unit='kg', ref_qty=2, cost_per_g=0.5)
        self.assertEqual(sc.cost_of_ref_qty, 1000)


class TestPersistableData(TestCase):
    def test_data_is_correct(self):
        # Check empty data;
        sc = fx.SupportsCostTestable()
        self.assertEqual(sc.persistable_data['cost_data'], model.cost.CostData(
            ref_qty=100,
            pref_unit='g',
            cost_per_g=None
        ))
        # Check when defined;
        sc = fx.SupportsCostTestable(ref_qty=150, pref_unit='mg', cost_per_g=12)
        self.assertEqual(sc.persistable_data['cost_data'], model.cost.CostData(
            ref_qty=150,
            pref_unit='mg',
            cost_per_g=12
        ))