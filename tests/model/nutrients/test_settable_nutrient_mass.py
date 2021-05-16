from unittest import TestCase

import model
from tests.model.nutrients import fixtures as fx


class TestConstructor(TestCase):
    @fx.use_test_nutrients
    def test_can_construct_instance(self):
        snm = model.nutrients.SettableNutrientMass("tirbur")
        self.assertTrue(isinstance(snm, model.nutrients.SettableNutrientMass))

    @fx.use_test_nutrients
    def test_loads_data_correctly(self):
        snm = model.nutrients.SettableNutrientMass(
            nutrient_name="tirbur",
            quantity_data=model.quantity.QuantityData(
                quantity_in_g=1.2,
                pref_unit="mg"
            )
        )
        self.assertEqual(1.2, snm._quantity_data['quantity_in_g'])
        self.assertEqual("mg", snm._quantity_data['pref_unit'])


class TestSetQuantity(TestCase):
    @fx.use_test_nutrients
    def test_sets_mass_correctly(self):
        snm = fx.init_settable_nutrient_mass("tirbur")
        snm.set_quantity(quantity=12, unit='mg')
        self.assertEqual(0.012, snm.quantity_in_g)
        self.assertEqual(12, snm.ref_qty)

    @fx.use_test_nutrients
    def test_sets_pref_unit_correctly(self):
        snm = fx.init_settable_nutrient_mass("tirbur")
        snm.set_quantity(quantity=12, unit='mg')
        self.assertEqual("mg", snm.pref_unit)

    @fx.use_test_nutrients
    def test_raises_exception_if_unit_not_mass(self):
        snm = fx.init_settable_nutrient_mass("tirbur")
        with self.assertRaises(model.quantity.exceptions.UnsupportedExtendedUnitsError):
            snm.set_quantity(quantity=1.2, unit="ml")
