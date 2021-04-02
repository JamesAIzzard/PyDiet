from unittest import TestCase

from model import ingredients


class TestSetDensity(TestCase):

    def setUp(self) -> None:
        self.ingredient = ingredients.Ingredient()

    def test_sets_density_correctly(self):
        # Check the density can be set;
        self.ingredient.set_density(2, 'kg', 2, 'L')
        self.assertAlmostEqual(self.ingredient.g_per_ml, 1, delta=0.0001)
        self.ingredient.set_density(2, 'kg', 1, 'L')
        self.assertAlmostEqual(self.ingredient.g_per_ml, 2, delta=0.0001)

    def test_sets_piece_mass_correctly(self):
        self.ingredient.piece_mass_g = 1000 # noqa
        self.ingredient.set_density(2, 'pc', 1, 'L')
        self.assertAlmostEqual(self.ingredient.g_per_ml, 2, delta=0.0001)
