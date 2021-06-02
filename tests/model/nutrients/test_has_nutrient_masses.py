"""Tests for the HasNutrientMasses class."""
from unittest import TestCase

import model.nutrients
from tests.model.nutrients import fixtures as fx
from tests.model.quantity import fixtures as qfx


class TestNumCalories(TestCase):
    """Tests the num_calories property."""
    @fx.use_test_nutrients
    def test_correct_num_calories_is_returned(self):
        """Checks that the method returns the correct number of calories."""
        # Create a test instance with a full set of calorie nutrients defined;
        hnm = fx.HasReadableNutrientMassesTestable(
            qty_subject=fx.HasReadableNutrientRatiosTestable(
                nutrient_ratios_data={
                    "tirbur": fx.get_nutrient_ratio_data(nutrient_mass_g=10, subject_qty_g=100),
                    "regatur": fx.get_nutrient_ratio_data(nutrient_mass_g=10, subject_qty_g=100),
                    "bazing": fx.get_nutrient_ratio_data(nutrient_mass_g=20, subject_qty_g=100),
                    "fillydon": fx.get_nutrient_ratio_data(nutrient_mass_g=30, subject_qty_g=100),
                    "busskie": fx.get_nutrient_ratio_data(nutrient_mass_g=10, subject_qty_g=100),
                    "bingtong": fx.get_nutrient_ratio_data(nutrient_mass_g=25, subject_qty_g=100)
                }
            ),
            quantity_data=qfx.get_qty_data(qty_in_g=90)
        )

    @fx.use_test_nutrients
    def test_raises_exception_if_calorie_nutrient_missing(self):
        """Checks we get an exception if one of the calorie nutrients are missing."""
        # Create a test instance with one of the calorie nutrients missing;
        hnm = fx.HasReadableNutrientMassesTestable(
            qty_subject=fx.HasReadableNutrientRatiosTestable(
                nutrient_ratios_data={
                    "tirbur": fx.get_nutrient_ratio_data(nutrient_mass_g=10, subject_qty_g=100),
                    "regatur": fx.get_nutrient_ratio_data(nutrient_mass_g=10, subject_qty_g=100),
                    "bazing": fx.get_nutrient_ratio_data(nutrient_mass_g=20, subject_qty_g=100),
                    "fillydon": fx.get_nutrient_ratio_data(nutrient_mass_g=30, subject_qty_g=100),
                    "bingtong": fx.get_nutrient_ratio_data(nutrient_mass_g=25, subject_qty_g=100)
                }
            ),
            quantity_data=qfx.get_qty_data(qty_in_g=90)
        )

        # Check we get an exception if we try at access the num calories;
        with self.assertRaises(model.nutrients.exceptions.UndefinedCalorieNutrientRatioError):
            _ = hnm.num_calories


class TestGetNutrientMassG(TestCase):
    """Tests the get_nutrient_mass_g method."""
    def test_correct_mass_is_returned(self):
        """Checks the method returns the correct nutrient mass."""
        # Create a test instance, with a specified nutrient ratio;
        hnm = fx.HasReadableNutrientMassesTestable(
            qty_subject=fx.HasReadableNutrientRatiosTestable(
                nutrient_ratios_data={
                    "protein": fx.get_nutrient_ratio_data(nutrient_mass_g=12, subject_qty_g=100)
                }
            ),
            quantity_data=qfx.get_qty_data(qty_in_g=50)
        )

        # Assert that we get the correct mass returned for that nutrient;
        self.assertEqual(6, hnm.get_nutrient_mass_g("protein"))

    def test_raises_exception_if_nutrient_mass_undefined(self):
        """Checks we get an exception if we try to access a nutrient mass which is undefined."""
        # Create a test instance;
        hnm = fx.HasReadableNutrientMassesTestable(
            qty_subject=fx.HasReadableNutrientRatiosTestable(
                nutrient_ratios_data={}
            ),
            quantity_data=qfx.get_qty_data(qty_in_g=50)
        )

        # Assert we get an exception if we try to access an undefined nutrient mass;
        with self.assertRaises(model.nutrients.exceptions.UndefinedNutrientRatioError):
            _ = hnm.get_nutrient_mass_g("protein")
