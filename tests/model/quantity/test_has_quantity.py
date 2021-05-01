from unittest import TestCase

import model
from tests.model.quantity import fixtures as fx


class TestQuantityInG(TestCase):

    def test_returns_corrrect_value(self):
        hq = fx.get_has_3kg()
        self.assertTrue(hq.quantity_in_g == 3000)

    def test_raises_exception_if_qty_in_g_undefined(self):
        hq = fx.get_undefined_has_quantity()
        with self.assertRaises(model.quantity.exceptions.UndefinedQuantityError):
            _ = hq.quantity_in_g


class TestQuantityPrefUnit(TestCase):

    def test_returns_correct_value(self):
        hq = fx.get_has_3kg()
        self.assertTrue(hq.quantity_pref_unit == 'kg')


class TestQuantityInPrefUnits(TestCase):
    def test_returns_correct_value(self):
        hq = fx.get_has_3kg()
        self.assertTrue(hq.quantity_in_pref_units == 3)

    def test_raises_exception_if_qty_undefined(self):
        hq = fx.get_undefined_has_quantity()
        with self.assertRaises(model.quantity.exceptions.UndefinedQuantityError):
            _ = hq.quantity_in_pref_units
