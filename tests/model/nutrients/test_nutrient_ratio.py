"""Tests for NutrientRatio class."""
from unittest import TestCase, mock

import model
from tests.model.nutrients import fixtures as fx


class TestConstructor(TestCase):
    """Tests the constructor function."""
    @fx.use_test_nutrients
    def test_can_instantiate(self):
        """Check we can instantiate an instance."""
        # Create a simple test instance;
        nr = model.nutrients.ReadonlyNutrientRatio(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            nutrient_ratio_data_src=fx.get_nutrient_ratio_data_src(fx.get_nutrient_ratio_data())
        )

        # Check the instance was created correctly;
        self.assertTrue(isinstance(nr, model.nutrients.ReadonlyNutrientRatio))

    @fx.use_test_nutrients
    def test_can_instantiate_with_data(self):
        """Check the instance has the correct data available, if data was passed in."""
        # Create a simple test instance;
        nr = model.nutrients.ReadonlyNutrientRatio(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            nutrient_ratio_data_src=fx.get_nutrient_ratio_data_src(fx.get_nutrient_ratio_data(
                nutrient_mass_g=20,
                nutrient_mass_unit="mg",
                subject_qty_g=100,
                subject_qty_unit='g'
            ))
        )

        # Check the instance has the correct data;
        self.assertEqual(20, nr.nutrient_mass.quantity_in_g)
        self.assertEqual("mg", nr.nutrient_mass.qty_pref_unit)
        self.assertEqual(100, nr.subject_ref_quantity.quantity_in_g)
        self.assertEqual("g", nr.subject_ref_quantity.qty_pref_unit)
