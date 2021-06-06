"""Tests for ReadonlyNutrientRatio class."""
from unittest import TestCase, mock

import model
from tests.model.nutrients import fixtures as nfx
from tests.model.quantity import fixtures as qfx


class TestConstructor(TestCase):
    """Tests the constructor function."""
    @nfx.use_test_nutrients
    def test_can_instantiate(self):
        """Check we can instantiate an instance."""
        # Create a simple test instance;
        nr = model.nutrients.ReadonlyNutrientRatio(
            ratio_host=mock.Mock(),
            nutrient_name="tirbur",
            qty_ratio_data_src=qfx.get_qty_ratio_data_src(qfx.get_qty_ratio_data())
        )

        # Check the instance was created correctly;
        self.assertTrue(isinstance(nr, model.nutrients.ReadonlyNutrientRatio))

    @nfx.use_test_nutrients
    def test_can_instantiate_with_data(self):
        """Check the instance has the correct data available, if data was passed in."""
        # Create a simple test instance;
        nr = model.nutrients.ReadonlyNutrientRatio(
            ratio_host=mock.Mock(),
            nutrient_name="tirbur",
            qty_ratio_data_src=qfx.get_qty_ratio_data_src(qfx.get_qty_ratio_data(
                subject_qty_g=20,
                subject_qty_unit="mg",
                host_qty_g=100,
                host_qty_unit='g'
            ))
        )

        # Check the instance has the correct data;
        self.assertEqual(20, nr.nutrient_mass.quantity_in_g)
        self.assertEqual("mg", nr.nutrient_mass.qty_pref_unit)
        self.assertEqual(100, nr.ratio_host_qty.quantity_in_g)
        self.assertEqual("g", nr.ratio_host_qty.qty_pref_unit)
