from unittest import TestCase

import model
from tests.model.nutrients import fixtures as fx


class TestConstructor(TestCase):
    @fx.use_test_nutrients
    def test_can_construct(self):
        nm = model.nutrients.NutrientMass(
            nutrient_name="tirbur",
            quantity_data_src=lambda: model.quantity.QuantityData(
                quantity_in_g=10,
                pref_unit='g'
            )
        )
        self.assertTrue(isinstance(nm, model.nutrients.NutrientMass))


class TestNutrient(TestCase):
    @fx.use_test_nutrients
    def test_nutrient_is_correct(self):
        nm = fx.init_10g_tirbur()
        self.assertTrue(nm.nutrient is fx.GLOBAL_NUTRIENTS["tirbur"])


class TestQtyInG(TestCase):
    @fx.use_test_nutrients
    def test_qty_is_correct(self):
        nm = fx.init_10g_tirbur()
        self.assertEqual(10, nm.quantity_in_g)


class TestPrefUnit(TestCase):
    @fx.use_test_nutrients
    def test_pref_unit_correct(self):
        nm = fx.init_100mg_docbe()
        self.assertEqual("mg", nm.pref_unit)


class TestRefQty(TestCase):
    @fx.use_test_nutrients
    def test_ref_qty_is_correct(self):
        nm = fx.init_100mg_docbe()
        self.assertEqual(100, nm.ref_qty)


class TestIsDefined(TestCase):
    @fx.use_test_nutrients
    def test_true_if_defined(self):
        self.assertTrue(fx.init_100mg_docbe().is_defined)

    @fx.use_test_nutrients
    def test_false_if_undefined(self):
        self.assertFalse(fx.init_undefined_docbe().is_defined)


class TestPersistableData(TestCase):
    @fx.use_test_nutrients
    def test_defined_data_is_correct(self):
        nm = fx.init_100mg_docbe()
        self.assertEqual(
            model.nutrients.NutrientMassData(
                quantity_in_g=0.1,
                pref_unit="mg"
            ),
            nm.persistable_data
        )

    @fx.use_test_nutrients
    def test_undefined_data_is_correct(self):
        nm = fx.init_undefined_docbe()
        self.assertEqual(
            model.nutrients.NutrientMassData(
                quantity_in_g=None,
                pref_unit="g"
            ),
            nm.persistable_data
        )
