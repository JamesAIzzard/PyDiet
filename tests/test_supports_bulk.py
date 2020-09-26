from unittest import TestCase

from pydiet import ingredients


class TestSetDensity(TestCase):

    def setUp(self):
        i_data = ingredients.ingredient.get_empty_ingredient_data()
        self.i = ingredients.ingredient.Ingredient(i_data)

    def test_sets_density_correctly(self):
        self.i.set_density(2, 'kg', 2, 'L')
        self.assertAlmostEqual(self.i.g_per_ml, 1, delta=0.0001)

        self.i.set_density(2, 'kg', 1, 'L')
        self.assertAlmostEqual(self.i.g_per_ml, 2, delta=0.0001)

    def test_sets_density_with_pc_correctly(self):
        self.i.set_piece_mass_g(1000)
        self.i.set_density(2, 'pc', 1, 'L')
        self.assertAlmostEqual(self.i.g_per_ml, 2, delta=0.0001)
