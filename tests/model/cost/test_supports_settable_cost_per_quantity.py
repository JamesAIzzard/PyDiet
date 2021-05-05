from unittest import TestCase

import model


class TestConstructor(TestCase):
    def test_correct_instance(self):
        self.assertTrue(model.cost.SupportsSettableCostPerQuantity(), model.cost.SupportsSettableCostPerQuantity)

    def test_loads_data(self):
        sc = model.cost.SupportsSettableCostPerQuantity(cost_per_qty_data=model.cost.CostPerQtyData(
            pref_unit='kg',
            quantity_in_g=1200,
            cost_per_g=0.25
        ))
        self.assertEqual(sc._cost_per_qty_data, model.cost.CostPerQtyData(
            pref_unit='kg',
            quantity_in_g=1200,
            cost_per_g=0.25
        ))


class TestSubjectQuantity(TestCase):
    def test_subject_quantity_is_settable(self):
        sc = model.cost.SupportsSettableCostPerQuantity()
        self.assertTrue(isinstance(sc.cost_ref_subject_quantity, model.quantity.SettableQuantityOf))


class TestSetCost(TestCase):
    def test_sets_cost_correctly(self):
        sc = model.cost.SupportsSettableCostPerQuantity()
        sc.set_cost(
            cost_gbp=12.50,
            qty=2,
            unit='kg'
        )
        self.assertEqual(sc.cost_per_g, 6.25 / 1000)
        self.assertEqual(sc.cost_ref_subject_quantity.pref_unit, 'kg')
        self.assertEqual(sc.cost_ref_subject_quantity.ref_qty, 2)

    def test_unsets_correctly(self):
        sc = model.cost.SupportsSettableCostPerQuantity(cost_per_qty_data=model.cost.CostPerQtyData(
            pref_unit='kg',
            quantity_in_g=1200,
            cost_per_g=0.25
        ))
        sc.set_cost(cost_gbp=None)
        self.assertEqual(sc._cost_per_g_, None)
