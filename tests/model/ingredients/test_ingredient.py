from unittest import TestCase
from typing import Union

import model


class TestDensityUnitsInUse(TestCase):
    def setUp(self) -> None:
        self.i = model.ingredients.Ingredient()

    def test_returns_false_if_not_in_use(self):
        self.assertTrue(self.i.density_is_defined is False)
        self.assertTrue(self.i.g_per_ml is None)
        self.assertTrue(self.i.density_units_in_use is False)

    def test_returns_correct_value(self):
        i: Union['model.quantity.HasSettableBulk', model.nutrients.HasSettableNutrientRatios] = self.i
        i.g_per_ml = 1.1
        self.assertTrue(i.density_is_defined is True)
        self.assertTrue(i.g_per_ml == 1.1)
        self.assertTrue(i.density_units_in_use is False)
        i.pref_unit = 'ml'
        self.assertTrue(i.density_units_in_use is True)
        i.pref_unit = 'g'
        self.assertTrue(i.density_units_in_use is False)


class TestPieceMassUnitsInUse(TestCase):
    def setUp(self) -> None:
        self.i = model.ingredients.Ingredient()

    def test_returns_false_if_not_in_use(self):
        self.assertTrue(self.i.piece_mass_defined is False)
        self.assertTrue(self.i.piece_mass_g is None)
        self.assertTrue(self.i.piece_mass_units_in_use is False)

    def test_returns_correct_value(self):
        i: Union['model.quantity.HasSettableBulk', model.nutrients.HasSettableNutrientRatios] = self.i
        i.piece_mass_g = 1.1
        self.assertTrue(i.piece_mass_defined is True)
        self.assertTrue(i.piece_mass_g == 1.1)
        self.assertTrue(i.piece_mass_units_in_use is False)
        i.pref_unit = 'pc'
        self.assertTrue(i.piece_mass_units_in_use is True)
        i.pref_unit = 'g'
        self.assertTrue(i.piece_mass_units_in_use is False)