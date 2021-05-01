from unittest import TestCase

import model
from tests.model.quantity import fixtures as fx


class TestDensityIsDefined(TestCase):
    def test_returns_true_if_density_defined(self):
        hb = fx.get_has_bulk_with_09_density()
        self.assertTrue(hb.density_is_defined)

    def test_returns_false_if_density_undefined(self):
        hb = model.quantity.HasBulk()
        self.assertFalse(hb.density_is_defined)


class TestPieceMassDefined(TestCase):
    def test_returns_true_if_piece_mass_defined(self):
        hb = fx.get_has_bulk_with_30_pc_mass()
        self.assertTrue(hb.piece_mass_defined)

    def test_returns_false_if_piece_mass_undefined(self):
        hb = model.quantity.HasBulk()
        self.assertFalse(hb.piece_mass_defined)
