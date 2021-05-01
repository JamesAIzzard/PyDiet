from unittest import TestCase

import model
from tests.model.nutrients import fixtures as fx


class TestConstructor(TestCase):
    def test_constructor_returns_instance(self):
        nm = model.nutrients.NutrientMass(nutrient=fx.get_protein())
        self.assertTrue(isinstance(nm, model.nutrients.NutrientMass))

    def test_constructor_loads_quantity_data(self):
        nm = model.nutrients.NutrientMass(
            nutrient=fx.get_protein(),
            nutrient_mass_data=model.nutrients.NutrientMassData(
                bulk_data=model.quantity.BulkData(
                    pref_unit='g',
                    ref_qty=100,
                    g_per_ml=None,
                    piece_mass_g=None
                ),
                quantity_in_g=32
            )
        )
        self.assertTrue(nm.quantity_in_g == 32)
        self.assertTrue(nm.pref_unit == 'g')
        self.assertTrue(nm.ref_qty == 100)
        self.assertFalse(nm.density_is_defined)
        self.assertFalse(nm.piece_mass_defined)

    def test_constructor_loads_nutrient_correctly(self):
        self.assertEqual(fx.get_32g_protein().nutrient, model.nutrients.GLOBAL_NUTRIENTS['protein'])


class TestIsDefined(TestCase):

    def test_returns_true_if_defined(self):
        self.assertTrue(fx.get_32g_protein().is_defined)

    def test_returns_false_if_not_defined(self):
        self.assertFalse(fx.get_undefined_protein_mass().is_defined)
