from unittest import TestCase

import model
from tests.model.nutrients import fixtures as fx

class TestQuantityPrefUnits(TestCase):

    def test_volume_qty_dissallowed(self):
        with self.assertRaises(model.quantity.exceptions.IncorrectUnitTypeError):
            fx.get_undefined_settable_protein_mass().pref_unit='L'
