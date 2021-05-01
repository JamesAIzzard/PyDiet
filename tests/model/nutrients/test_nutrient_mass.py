from unittest import TestCase

import model
from tests.model.nutrients import fixtures as fx


class TestConstructor(TestCase):
    def test_constructor_returns_instance(self):
        self.assertTrue(isinstance(fx.get_undefined_protein_mass(), model.nutrients.NutrientMass))

    def test_constructor_loads_nutrient_correctly(self):
        self.assertEqual(fx.get_32g_protein().nutrient, model.nutrients.GLOBAL_NUTRIENTS['protein'])


class TestNutrient(TestCase):
    def test_nutrient_returned_correctly(self):
        nm = fx.get_32g_protein()
        self.assertTrue(nm.nutrient is model.nutrients.GLOBAL_NUTRIENTS['protein'])


class TestIsDefined(TestCase):

    def test_returns_true_if_defined(self):
        self.assertTrue(fx.get_32g_protein().is_defined)

    def test_returns_false_if_not_defined(self):
        self.assertFalse(fx.get_undefined_protein_mass().is_defined)
