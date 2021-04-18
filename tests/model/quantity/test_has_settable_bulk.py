from unittest import TestCase

import model
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

    def test_cannot_set_zero(self):
        with self.assertRaises(model.quantity.exceptions.ZeroQtyError):
            self.ingredient.set_density(0, 'kg', 4, 'L')
        with self.assertRaises(model.quantity.exceptions.ZeroQtyError):
            self.ingredient.set_density(4, 'kg', 0, 'L')
        with self.assertRaises(model.quantity.exceptions.ZeroQtyError):
            self.ingredient.set_density(0, 'kg', 0, 'L')


class TestSetPieceMass(TestCase):

    def setUp(self) -> None:
        self.ingredient = ingredients.Ingredient()

    def test_sets_piece_mass_correctly(self):
        ingredient: 'model.quantity.HasSettableBulk' = self.ingredient
        ingredient.piece_mass_g = 1000
        ingredient.set_density(2, 'pc', 1, 'L')
        self.assertAlmostEqual(self.ingredient.g_per_ml, 2, delta=0.0001)

    def test_cannot_set_zero(self):
        with self.assertRaises(model.quantity.exceptions.ZeroQtyError):
            self.ingredient.set_piece_mass(0, 2, 'kg')
        with self.assertRaises(model.quantity.exceptions.ZeroQtyError):
            self.ingredient.set_piece_mass(4, 0, 'kg')
        with self.assertRaises(model.quantity.exceptions.ZeroQtyError):
            self.ingredient.set_piece_mass(0, 0, 'kg')
