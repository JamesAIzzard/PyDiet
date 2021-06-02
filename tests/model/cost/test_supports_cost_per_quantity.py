from unittest import TestCase

import model
from tests.model.cost import fixtures as fx


class TestConstructor(TestCase):
    def test_correct_type(self):
        self.assertTrue(isinstance(fx.HasReadableCostPerQuantityTestable(), model.cost.HasReadableCostPerQuantity))


class TestSubjectQuantity(TestCase):
    def test_instance_has_correct_values(self):
        sc = fx.HasReadableCostPerQuantityTestable(
            pref_unit='kg',
            ref_qty_g=120,
            cost_per_g=0.025
        )
        self.assertEqual(sc.cost_ref_subject_quantity.quantity_in_g, 120)
        self.assertEqual(sc.cost_ref_subject_quantity.qty_pref_unit, 'kg')


class TestCostPerG(TestCase):
    def test_result_is_correct(self):
        sc = fx.HasReadableCostPerQuantityTestable(cost_per_g=0.25)
        self.assertEqual(sc.cost_per_g, 0.25)

    def test_raises_exception_if_undefined(self):
        sc = fx.HasReadableCostPerQuantityTestable()
        with self.assertRaises(model.cost.exceptions.UndefinedCostError):
            _ = sc.cost_per_g


class TestCostPerPrefUnit(TestCase):
    def test_result_is_correct(self):
        sc = fx.HasReadableCostPerQuantityTestable(pref_unit='kg', cost_per_g=0.5)
        self.assertEqual(sc.cost_per_pref_unit, 500)


class TestCostOfRefQty(TestCase):
    def test_result_is_correct(self):
        sc = fx.HasReadableCostPerQuantityTestable(pref_unit='kg', ref_qty_g=2000, cost_per_g=0.5)
        self.assertEqual(sc.cost_of_ref_qty, 1000)


class TestPersistableData(TestCase):
    def test_data_is_correct(self):
        # Check empty data;
        sc = fx.HasReadableCostPerQuantityTestable(ref_qty_g=None, cost_per_g=None)
        self.assertEqual(sc.persistable_data['cost_per_qty_data'], model.cost.CostPerQtyData(
            pref_unit='g',
            quantity_in_g=None,
            cost_per_g=None
        ))
        # Check when defined;
        sc = fx.HasReadableCostPerQuantityTestable(pref_unit='kg', ref_qty_g=2000, cost_per_g=0.5)
        self.assertEqual(sc.persistable_data['cost_per_qty_data'], model.cost.CostPerQtyData(
            pref_unit='kg',
            quantity_in_g=2000,
            cost_per_g=0.5
        ))
