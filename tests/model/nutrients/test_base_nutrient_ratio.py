"""Tests for the BaseNutrientRatio class."""
from unittest import TestCase, mock

import model
from tests.model.nutrients import fixtures as fx


class TestGPerSubjectG(TestCase):
    """Tests the g_per_subject_g property."""

    @fx.use_test_nutrients
    def test_g_per_subject_g_is_correct_when_non_zero(self):
        """Check a non-zero nutrient mass yields the correct ratio."""
        # Create a test instance with non-zero mass data;
        bnr = fx.BaseNutrientRatioTestable(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            nutrient_ratio_data=fx.get_nutrient_ratio_data(
                nutrient_mass_g=12,
                nutrient_mass_unit="mg",
                subject_qty_g=120,
                subject_qty_unit="lb"
            )
        )

        # Assert we get the correct ratio back;
        self.assertEqual(0.1, bnr.g_per_subject_g)

    @fx.use_test_nutrients
    def test_g_per_subject_g_is_correct_when_zero(self):
        """Check that we get a zero ratio when the nutrient mass is zero."""
        # Create a test instance with zero nutrient mass;
        bnr = fx.BaseNutrientRatioTestable(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            nutrient_ratio_data=fx.get_nutrient_ratio_data(
                nutrient_mass_g=0,
                subject_qty_g=120,
            )
        )

        # Check the ratio is zero;
        self.assertEqual(0, bnr.g_per_subject_g)

    @fx.use_test_nutrients
    def test_raises_exception_if_nutrient_mass_is_not_defined(self):
        """Check we get an exception if the nutrient mass is not defined;"""
        # Create a test instance with undefined nutrient mass;
        bnr = fx.BaseNutrientRatioTestable(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            nutrient_ratio_data=fx.get_nutrient_ratio_data()
        )

        # Assert the exception is raised when we try to access;
        with self.assertRaises(model.nutrients.exceptions.UndefinedNutrientRatioError):
            _ = bnr.g_per_subject_g


class TestMassInNutrientPrefUnitPerSubjectG(TestCase):
    """Tests for mass_in_nutrient_pref_unit_per_subject_g."""

    @fx.use_test_nutrients
    def test_correct_value_is_returned_for_non_zero_mass(self):
        """Check we get the correct value from the method when the nutrient mass is not zero."""
        # Create a test instance with non-zero mass data;
        bnr = fx.BaseNutrientRatioTestable(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            nutrient_ratio_data=fx.get_nutrient_ratio_data(
                nutrient_mass_g=0.012,
                nutrient_mass_unit="mg",
                subject_qty_g=100,
                subject_qty_unit="g"
            )
        )

        # Check the correct value is returned;
        self.assertAlmostEqual(0.12, bnr.mass_in_nutrient_pref_unit_per_subject_g, delta=0.001)

    @fx.use_test_nutrients
    def test_correct_value_is_returned_for_zero_mass(self):
        """Check we get the correct value from the method when the nutrient mass is not zero."""
        # Create a test instance with non-zero mass data;
        bnr = fx.BaseNutrientRatioTestable(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            nutrient_ratio_data=fx.get_nutrient_ratio_data(
                nutrient_mass_g=0,
                subject_qty_g=100,
            )
        )

        # Check the correct value is returned;
        self.assertEqual(0, bnr.mass_in_nutrient_pref_unit_per_subject_g)

    @fx.use_test_nutrients
    def test_raises_exception_if_nutrient_mass_is_not_defined(self):
        """Check we get an exception if the nutrient mass is not defined;"""
        # Create a test instance with undefined nutrient mass;
        bnr = fx.BaseNutrientRatioTestable(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            nutrient_ratio_data=fx.get_nutrient_ratio_data()
        )

        # Assert the exception is raised when we try to access;
        with self.assertRaises(model.nutrients.exceptions.UndefinedNutrientRatioError):
            _ = bnr.mass_in_nutrient_pref_unit_per_subject_g


class TestMassInNutrientPrefUnitPerSubjectReqQty(TestCase):
    """Tests the mass_in_nutrient_pref_unit_per_subject_qty property."""

    @fx.use_test_nutrients
    def test_correct_value_is_returned_for_non_zero_mass(self):
        """Check we get the correct value when the nutrient mass is non-zero."""
        # Create a test instance with non-zero mass data;
        bnr = fx.BaseNutrientRatioTestable(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            nutrient_ratio_data=fx.get_nutrient_ratio_data(
                nutrient_mass_g=0.012,
                nutrient_mass_unit="mg",
                subject_qty_g=100,
                subject_qty_unit="g"
            )
        )

        # Check the correct value is returned;
        self.assertAlmostEqual(12, bnr.mass_in_nutrient_pref_unit_per_subject_ref_qty, delta=0.001)

    @fx.use_test_nutrients
    def test_correct_value_is_returned_for_zero_mass(self):
        """Check we get the correct value from the method when the nutrient mass is not zero."""
        # Create a test instance with non-zero mass data;
        bnr = fx.BaseNutrientRatioTestable(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            nutrient_ratio_data=fx.get_nutrient_ratio_data(
                nutrient_mass_g=0,
                subject_qty_g=100,
            )
        )

        # Check the correct value is returned;
        self.assertEqual(0, bnr.mass_in_nutrient_pref_unit_per_subject_ref_qty)

    @fx.use_test_nutrients
    def test_raises_exception_if_nutrient_mass_is_not_defined(self):
        """Check we get an exception if the nutrient mass is not defined;"""
        # Create a test instance with undefined nutrient mass;
        bnr = fx.BaseNutrientRatioTestable(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            nutrient_ratio_data=fx.get_nutrient_ratio_data()
        )

        # Assert the exception is raised when we try to access;
        with self.assertRaises(model.nutrients.exceptions.UndefinedNutrientRatioError):
            _ = bnr.mass_in_nutrient_pref_unit_per_subject_ref_qty


class TestRatioIsDefined(TestCase):
    """Tests the is_defined property."""

    @fx.use_test_nutrients
    def test_returns_true_if_nutrient_ratio_defined(self):
        """Check we get a True value if the nutrient ratio is defined."""
        # Create a test instance with the nutrient ratio defined;
        bnr = fx.BaseNutrientRatioTestable(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            nutrient_ratio_data=fx.get_nutrient_ratio_data(
                nutrient_mass_g=0.02,
                nutrient_mass_unit="kg",
                subject_qty_g=100,
                subject_qty_unit="g"
            )
        )

        # Assert we get a True result;
        self.assertTrue(bnr.ratio_is_defined)

    @fx.use_test_nutrients
    def test_returns_false_if_nutrient_ratio_defined(self):
        """Check we get a False value if the nutrient ratio is defined."""
        # Create a test instance with the nutrient ratio defined;
        bnr = fx.BaseNutrientRatioTestable(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            nutrient_ratio_data=fx.get_nutrient_ratio_data(nutrient_mass_g=None)
        )

        # Assert we get a False result;
        self.assertFalse(bnr.ratio_is_defined)


class TestRatioIsZero(TestCase):
    """Tests the is_zero property."""

    @fx.use_test_nutrients
    def test_returns_true_if_nutrient_zero(self):
        """Checks the return value is True if the nutrient mass is zero;"""
        # Create a test instance with the nutrient ratio defined;
        bnr = fx.BaseNutrientRatioTestable(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            nutrient_ratio_data=fx.get_nutrient_ratio_data(
                nutrient_mass_g=0,
                subject_qty_g=100
            )
        )

        # Assert we get a True result;
        self.assertTrue(bnr.ratio_is_zero)

    @fx.use_test_nutrients
    def test_returns_false_if_nutrient_non_zero(self):
        """Checks the return value is False if the nutrient mass is non_zero;"""
        # Create a test instance with the nutrient ratio defined;
        bnr = fx.BaseNutrientRatioTestable(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            nutrient_ratio_data=fx.get_nutrient_ratio_data(
                nutrient_mass_g=0.012,
                nutrient_mass_unit="mg",
                subject_qty_g=100,
                subject_qty_unit="g"
            )
        )

        # Assert we get a False result;
        self.assertFalse(bnr.ratio_is_zero)


class TestPersistableData(TestCase):
    """Tests the persistable data property."""

    @fx.use_test_nutrients
    def test_returns_correct_data(self):
        """Check we get the correct data from the property."""
        # Create some data to pass in;
        data = fx.get_nutrient_ratio_data(
            nutrient_mass_g=0.012,
            nutrient_mass_unit="mg",
            subject_qty_g=100,
            subject_qty_unit="g"
        )

        # Create the test instance, passing the test data in;
        bnr = fx.BaseNutrientRatioTestable(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            nutrient_ratio_data=data
        )

        # Check we get the same data back out;
        self.assertEqual(data, bnr.persistable_data)
