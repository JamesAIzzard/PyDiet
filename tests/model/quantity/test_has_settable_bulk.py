from unittest import TestCase

import model
from model import ingredients


class TestSetRefQty(TestCase):
    def setUp(self) -> None:
        self.ingredient: 'model.quantity.HasSettableBulk' = ingredients.Ingredient()

    def test_sets_ref_qty_correctly(self):
        self.ingredient.ref_qty = 1.5
        self.ingredient.pref_unit = 'kg'
        self.assertEqual(self.ingredient.ref_qty, 1.5)
        self.assertEqual(self.ingredient.pref_unit, 'kg')

    def test_prevents_zero_ref_qty(self):
        with self.assertRaises(model.quantity.exceptions.ZeroQtyError):
            self.ingredient.ref_qty = 0


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


class TestSetGPerMl(TestCase):

    def setUp(self) -> None:
        self.ingredient: 'model.quantity.HasSettableBulk' = ingredients.Ingredient()

    def test_sets_correctly(self):
        self.ingredient.g_per_ml = 1.2
        self.assertEqual(self.ingredient.g_per_ml, 1.2)

    def test_cannot_set_zero(self):
        with self.assertRaises(model.quantity.exceptions.ZeroQtyError):
            self.ingredient.g_per_ml = 0


class TestSetPieceMass(TestCase):

    def setUp(self) -> None:
        self.ingredient = ingredients.Ingredient()

    def test_sets_piece_mass_correctly(self):
        ingredient: 'model.quantity.HasSettableBulk' = self.ingredient
        ingredient.piece_mass_g = 1000
        ingredient.set_piece_mass(
            num_pieces=4,
            mass_qty=8,
            mass_unit='kg'
        )
        self.assertAlmostEqual(self.ingredient.piece_mass_g, 2000, delta=0.0001)

    def test_cannot_set_zero(self):
        with self.assertRaises(model.quantity.exceptions.ZeroQtyError):
            self.ingredient.set_piece_mass(0, 2, 'kg')
        with self.assertRaises(model.quantity.exceptions.ZeroQtyError):
            self.ingredient.set_piece_mass(4, 0, 'kg')
        with self.assertRaises(model.quantity.exceptions.ZeroQtyError):
            self.ingredient.set_piece_mass(0, 0, 'kg')


class TestSetPieceMassG(TestCase):
    def setUp(self) -> None:
        self.ingredient: 'model.quantity.HasSettableBulk' = ingredients.Ingredient()

    def test_sets_correctly(self):
        self.ingredient.piece_mass_g = 120
        self.assertEqual(self.ingredient.piece_mass_g, 120)

    def test_cannot_set_zero(self):
        with self.assertRaises(model.quantity.exceptions.ZeroQtyError):
            self.ingredient.piece_mass_g = 0

