"""Tests for the NutrientRatioBase class."""
from unittest import TestCase, mock

import model
from tests.model.nutrients import fixtures as nfx
from tests.model.quantity import fixtures as qfx


class TestSubjectGPerHostG(TestCase):
    """Tests the subject_g_per_host_g property."""

    @nfx.use_test_nutrients
    def test_value_is_correct_when_non_zero(self):
        """Check a non-zero nutrient mass yields the correct ratio."""
        # Create a test instance with non-zero mass data;
        bnr = nfx.NutrientRatioBaseTestable(
            nutrient_name="foo",
            ratio_host=mock.Mock(),
            quantity_ratio_data=qfx.get_qty_ratio_data(
                subject_qty_g=10,
                subject_qty_unit='g',
                host_qty_g=100,
                host_qty_unit='g'
            )
        )

        # Assert we get the correct ratio back;
        self.assertEqual(0.1, bnr.subject_g_per_host_g)

    @nfx.use_test_nutrients
    def test_g_per_subject_g_is_correct_when_zero(self):
        """Check that we get a zero ratio when the nutrient mass is zero."""
        # Create a test instance with zero nutrient mass;
        bnr = nfx.NutrientRatioBaseTestable(
            nutrient_name="foo",
            ratio_host=mock.Mock(),
            quantity_ratio_data=qfx.get_qty_ratio_data(
                subject_qty_g=0,
                subject_qty_unit='g',
                host_qty_g=100,
                host_qty_unit='g'
            )
        )

        # Check the ratio is zero;
        self.assertEqual(0, bnr.subject_g_per_host_g)

    @nfx.use_test_nutrients
    def test_raises_exception_if_nutrient_mass_is_not_defined(self):
        """Check we get an exception if the nutrient mass is not defined;"""
        # Create a test instance with undefined nutrient mass;
        bnr = nfx.NutrientRatioBaseTestable(
            nutrient_name="foo",
            ratio_host=mock.Mock(),
            quantity_ratio_data=qfx.get_qty_ratio_data()
        )

        # Assert the exception is raised when we try to access;
        with self.assertRaises(model.nutrients.exceptions.UndefinedNutrientRatioError):
            _ = bnr.subject_g_per_host_g


class TestSubjectQtyInPrefUnitPerGOfHost(TestCase):
    """Tests for mass_in_nutrient_pref_unit_per_subject_g."""

    @nfx.use_test_nutrients
    def test_correct_value_is_returned_for_non_zero_mass(self):
        """Check we get the correct value from the method when the nutrient mass is not zero."""
        # Create a test instance with non-zero mass data;
        bnr = nfx.NutrientRatioBaseTestable(
            nutrient_name="tirbur",
            ratio_host=mock.Mock(),
            quantity_ratio_data=qfx.get_qty_ratio_data(
                subject_qty_g=0.012,
                subject_qty_unit='mg',
                host_qty_g=100,
                host_qty_unit='g'
            )
        )

        # Check the correct value is returned;
        self.assertAlmostEqual(0.12, bnr.subject_qty_in_pref_unit_per_g_of_host, delta=0.001)

    @nfx.use_test_nutrients
    def test_correct_value_is_returned_for_zero_mass(self):
        """Check we get the correct value from the method when the nutrient mass is not zero."""
        # Create a test instance with non-zero mass data;
        bnr = nfx.NutrientRatioBaseTestable(
            nutrient_name="tirbur",
            ratio_host=mock.Mock(),
            quantity_ratio_data=qfx.get_qty_ratio_data(
                subject_qty_g=0,
                host_qty_g=100,
            )
        )

        # Check the correct value is returned;
        self.assertEqual(0, bnr.subject_qty_in_pref_unit_per_g_of_host)

    @nfx.use_test_nutrients
    def test_raises_exception_if_nutrient_mass_is_not_defined(self):
        """Check we get an exception if the nutrient mass is not defined;"""
        # Create a test instance with undefined nutrient mass;
        bnr = nfx.NutrientRatioBaseTestable(
            nutrient_name="tirbur",
            ratio_host=mock.Mock(),
            quantity_ratio_data=qfx.get_qty_ratio_data()
        )

        # Assert the exception is raised when we try to access;
        with self.assertRaises(model.nutrients.exceptions.UndefinedNutrientRatioError):
            _ = bnr.subject_qty_in_pref_unit_per_g_of_host


class TestMassInNutrientPrefUnitPerSubjectReqQty(TestCase):
    """Tests the mass_in_nutrient_pref_unit_per_subject_qty property."""

    @nfx.use_test_nutrients
    def test_correct_value_is_returned_for_non_zero_mass(self):
        """Check we get the correct value when the nutrient mass is non-zero."""
        # Create a test instance with non-zero mass data;
        bnr = nfx.NutrientRatioBaseTestable(
            nutrient_name="tirbur",
            ratio_host=mock.Mock(),
            quantity_ratio_data=qfx.get_qty_ratio_data(
                subject_qty_g=0.012,
                subject_qty_unit='mg',
                host_qty_g=100,
                host_qty_unit='g'
            )
        )

        # Check the correct value is returned;
        self.assertAlmostEqual(12, bnr.subject_qty_in_pref_unit_per_ref_qty_of_host, delta=0.001)

    @nfx.use_test_nutrients
    def test_correct_value_is_returned_for_zero_mass(self):
        """Check we get the correct value from the method when the nutrient mass is not zero."""
        # Create a test instance with non-zero mass data;
        bnr = nfx.NutrientRatioBaseTestable(
            nutrient_name="tirbur",
            ratio_host=mock.Mock(),
            quantity_ratio_data=qfx.get_qty_ratio_data(
                subject_qty_g=0,
                host_qty_g=100,
            )
        )

        # Check the correct value is returned;
        self.assertEqual(0, bnr.subject_qty_in_pref_unit_per_ref_qty_of_host)

    @nfx.use_test_nutrients
    def test_raises_exception_if_nutrient_mass_is_not_defined(self):
        """Check we get an exception if the nutrient mass is not defined;"""
        # Create a test instance with undefined nutrient mass;
        bnr = nfx.NutrientRatioBaseTestable(
            nutrient_name="tirbur",
            ratio_host=mock.Mock(),
            quantity_ratio_data=qfx.get_qty_ratio_data()
        )

        # Assert the exception is raised when we try to access;
        with self.assertRaises(model.nutrients.exceptions.UndefinedNutrientRatioError):
            _ = bnr.subject_qty_in_pref_unit_per_ref_qty_of_host


class TestRatioIsDefined(TestCase):
    """Tests the is_defined property."""

    @nfx.use_test_nutrients
    def test_returns_true_if_nutrient_ratio_defined(self):
        """Check we get a True value if the nutrient ratio is defined."""
        # Create a test instance with the nutrient ratio defined;
        bnr = nfx.NutrientRatioBaseTestable(
            nutrient_name="tirbur",
            ratio_host=mock.Mock(),
            quantity_ratio_data=qfx.get_qty_ratio_data(
                subject_qty_g=0.02,
                subject_qty_unit='kg',
                host_qty_g=100,
                host_qty_unit='g'
            )
        )

        # Assert we get a True result;
        self.assertTrue(bnr.ratio_is_defined)

    @nfx.use_test_nutrients
    def test_returns_false_if_nutrient_ratio_defined(self):
        """Check we get a False value if the nutrient ratio is defined."""
        # Create a test instance with the nutrient ratio defined;
        bnr = nfx.NutrientRatioBaseTestable(
            nutrient_name="tirbur",
            ratio_host=mock.Mock(),
            quantity_ratio_data=qfx.get_qty_ratio_data()
        )

        # Assert we get a False result;
        self.assertFalse(bnr.ratio_is_defined)


class TestRatioIsZero(TestCase):
    """Tests the is_zero property."""

    @nfx.use_test_nutrients
    def test_returns_true_if_nutrient_zero(self):
        """Checks the return value is True if the nutrient mass is zero;"""
        # Create a test instance with the nutrient ratio defined;
        bnr = nfx.NutrientRatioBaseTestable(
            nutrient_name="tirbur",
            ratio_host=mock.Mock(),
            quantity_ratio_data=qfx.get_qty_ratio_data(
                subject_qty_g=0,
                subject_qty_unit='kg',
                host_qty_g=100,
                host_qty_unit='g'
            )
        )

        # Assert we get a True result;
        self.assertTrue(bnr.ratio_is_zero)

    @nfx.use_test_nutrients
    def test_returns_false_if_nutrient_non_zero(self):
        """Checks the return value is False if the nutrient mass is non_zero;"""
        # Create a test instance with the nutrient ratio defined;
        bnr = nfx.NutrientRatioBaseTestable(
            nutrient_name="tirbur",
            ratio_host=mock.Mock(),
            quantity_ratio_data=qfx.get_qty_ratio_data(
                subject_qty_g=0.02,
                subject_qty_unit='kg',
                host_qty_g=100,
                host_qty_unit='g'
            )
        )

        # Assert we get a False result;
        self.assertFalse(bnr.ratio_is_zero)


class TestPersistableData(TestCase):
    """Tests the persistable data property."""

    @nfx.use_test_nutrients
    def test_returns_correct_data(self):
        """Check we get the correct data from the property."""
        # Create some data to pass in;
        data = qfx.get_qty_ratio_data(
            subject_qty_g=0.012,
            subject_qty_unit="mg",
            host_qty_g=100,
            host_qty_unit="g"
        )

        # Create the test instance, passing the test data in;
        bnr = nfx.NutrientRatioBaseTestable(
            nutrient_name="tirbur",
            ratio_host=mock.Mock(),
            quantity_ratio_data=data
        )

        # Check we get the same data back out;
        self.assertEqual(data, bnr.persistable_data)
