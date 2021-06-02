"""Tests for the SettableNutrientRatio class."""
from unittest import TestCase, mock

import model
from tests.model.nutrients import fixtures as fx
from tests.model.quantity import fixtures as qfx


class TestConstructor(TestCase):
    """Test the constructor function;"""

    @fx.use_test_nutrients
    def test_can_construct_instance(self):
        """Checks that we can construct an instance."""
        # Create a simple test instance;
        snr = model.nutrients.SettableNutrientRatio(nutrient_name="tirbur", subject=mock.Mock())

        # Assert the instance was created successfully;
        self.assertTrue(isinstance(snr, model.nutrients.SettableNutrientRatio))

    @fx.use_test_nutrients
    def test_loads_data_if_provided(self):
        """Checks that any data passed in is available on the instance."""
        # Create an instance, passing the data in;
        snr = model.nutrients.SettableNutrientRatio(
            nutrient_name="tirbur",
            subject=mock.Mock(),
            nutrient_ratio_data=fx.get_nutrient_ratio_data(
                nutrient_mass_g=0.012,
                nutrient_mass_unit="mg",
                subject_qty_g=120,
                subject_qty_unit="kg"
            )
        )

        # Check the values on the instance are correct;
        self.assertEqual(0.012, snr.nutrient_mass.quantity_in_g)
        self.assertEqual("mg", snr.nutrient_mass.qty_pref_unit)
        self.assertEqual(120, snr.subject_ref_quantity.quantity_in_g)
        self.assertEqual("kg", snr.subject_ref_quantity.qty_pref_unit)


class TestSetRatio(TestCase):
    """Tests the set_ratio method."""

    @fx.use_test_nutrients
    def test_valid_data_is_set_correctly(self):
        """Checks that valid data can be set correctly."""
        # Create a test instance;
        snr = model.nutrients.SettableNutrientRatio(
            nutrient_name="tirbur",
            subject=mock.Mock()
        )

        # Assert that the nutrient ratio is undefined to start with;
        self.assertFalse(snr.ratio_is_defined)

        # Set a the nutrient ratio with valid data;
        snr.set_ratio(
            nutrient_mass=12,
            nutrient_mass_unit="mg",
            subject_qty=0.1,
            subject_qty_unit="kg"
        )

        # Check the correct values were set;
        self.assertEqual(0.012, snr.nutrient_mass.quantity_in_g)
        self.assertEqual("mg", snr.nutrient_mass.qty_pref_unit)
        self.assertEqual(100, snr.subject_ref_quantity.quantity_in_g)
        self.assertEqual("kg", snr.subject_ref_quantity.qty_pref_unit)

    @fx.use_test_nutrients
    def test_subject_qty_can_be_volume_if_configured(self):
        """Checks that valid data can include volumetric units if the subject supports test units."""
        # Create a test instance that supports extended units;
        snr = model.nutrients.SettableNutrientRatio(
            nutrient_name="tirbur",
            subject=qfx.HasReadableExtendedUnitsTestable(g_per_ml=1.5)
        )

        # Assert that the nutrient ratio is undefined to start with;
        self.assertFalse(snr.ratio_is_defined)

        # Now set the ratio, using volumetric units for the subject qty;
        snr.set_ratio(
            nutrient_mass=12,
            nutrient_mass_unit="mg",
            subject_qty=0.5,
            subject_qty_unit="L"
        )

        # Now check that the correct values were set;
        self.assertEqual(0.012, snr.nutrient_mass.quantity_in_g)
        self.assertEqual("mg", snr.nutrient_mass.qty_pref_unit)
        self.assertEqual(750, snr.subject_ref_quantity.quantity_in_g)
        self.assertEqual("l", snr.subject_ref_quantity.qty_pref_unit)

    @fx.use_test_nutrients
    def test_exception_if_subject_qty_is_volume_and_not_configured(self):
        """Checks that an exception is raised if we use volumetric units and the subject does not have
        density configured."""
        # Create a test instance, with a subject that supports extended units, but does not have them configured;
        snr = model.nutrients.SettableNutrientRatio(
            nutrient_name="tirbur",
            subject=qfx.HasReadableExtendedUnitsTestable(g_per_ml=None)
        )

        # Assert we get an exception if we try to use volumetric units;
        with self.assertRaises(model.quantity.exceptions.UndefinedDensityError):
            snr.set_ratio(
                nutrient_mass=12,
                nutrient_mass_unit="mg",
                subject_qty=0.5,
                subject_qty_unit="L"
            )

    @fx.use_test_nutrients
    def test_exception_if_subject_unit_is_extended_and_extended_units_not_supported(self):
        """Checks that an exception is raised if we use extended units and the subject does not
        support extended units."""
        # Create a test instance, with a subject that does not support extended units;
        snr = model.nutrients.SettableNutrientRatio(
            nutrient_name="tirbur",
            subject=mock.Mock()
        )

        # Assert we get an exception if we try to use volumetric units;
        with self.assertRaises(model.quantity.exceptions.UnsupportedExtendedUnitsError):
            snr.set_ratio(
                nutrient_mass=12,
                nutrient_mass_unit="mg",
                subject_qty=0.5,
                subject_qty_unit="L"
            )

    @fx.use_test_nutrients
    def test_exception_if_nutrient_mass_unit_is_not_a_mass(self):
        """Check we get an exception if we use a unit that is not a mass for the nutrient mass unit."""
        # Create a test instance with a subject that has an extended unit defined;
        snr = model.nutrients.SettableNutrientRatio(
            nutrient_name="tirbur",
            subject=qfx.HasReadableExtendedUnitsTestable(g_per_ml=1.1)
        )

        # Check that, even with ext unit defined on subject, the mass still has to be a mass;
        with self.assertRaises(model.quantity.exceptions.UnsupportedExtendedUnitsError):
            snr.set_ratio(
                nutrient_mass=12,
                nutrient_mass_unit="L",
                subject_qty=0.5,
                subject_qty_unit="L"
            )

    @fx.use_test_nutrients
    def test_exception_if_subject_quantity_is_zero(self):
        """Checks that an exception is raised if we try and set a nutrient ratio against a
        zero subject quantity."""
        # Create the instance;
        snr = model.nutrients.SettableNutrientRatio(
            nutrient_name="tirbur",
            subject=mock.Mock()
        )

        # Set with zero subject qty, and check we get an error;
        with self.assertRaises(model.quantity.exceptions.ZeroQtyError):
            snr.set_ratio(
                nutrient_mass=0,
                nutrient_mass_unit="g",
                subject_qty=0,
                subject_qty_unit="g"
            )


class TestUndefine(TestCase):
    """Tests the undefine method."""

    @fx.use_test_nutrients
    def test_nutrient_ratio_undefined_correctly(self):
        """Check that the nutrient ratio is undefined when the method is called."""
        # Create a nutrient ratio instance, passing in some data;
        snr = model.nutrients.SettableNutrientRatio(
            nutrient_name="tirbur",
            subject=mock.Mock(),
            nutrient_ratio_data=fx.get_nutrient_ratio_data(
                nutrient_mass_g=0.012,
                nutrient_mass_unit="mg",
                subject_qty_g=120,
                subject_qty_unit="kg"
            )
        )

        # Assert that the ratio is defined;
        self.assertTrue(snr.ratio_is_defined)

        # Undefine it;
        snr.undefine()

        # Assert that the ratio has been undefined;
        self.assertFalse(snr.ratio_is_defined)


class TestZero(TestCase):
    """Tests the zero method."""

    @fx.use_test_nutrients
    def test_nutrient_ratio_zeroed_correctly(self):
        """Checks that the nutrient mass is zeroed when the method is called."""
        # Create a test instance with non-zero values;
        # Create a nutrient ratio instance, passing in some data;
        snr = model.nutrients.SettableNutrientRatio(
            nutrient_name="tirbur",
            subject=mock.Mock(),
            nutrient_ratio_data=fx.get_nutrient_ratio_data(
                nutrient_mass_g=0.012,
                nutrient_mass_unit="mg",
                subject_qty_g=120,
                subject_qty_unit="kg"
            )
        )

        # Assert that the instance is non-zero;
        self.assertEqual(0.012, snr.nutrient_mass.quantity_in_g)

        # Call the zero() method;
        snr.zero()

        # Assert that the instance is now zero;
        self.assertEqual(0, snr.nutrient_mass.quantity_in_g)
        self.assertTrue(snr.ratio_is_zero)


class TestLoadData(TestCase):
    """Tests the load_data method."""

    @fx.use_test_nutrients
    def test_load_data(self):
        """Checks that data is loaded correctly;"""
        # Create some test data;
        data = fx.get_nutrient_ratio_data(
            nutrient_mass_g=0.012,
            nutrient_mass_unit="mg",
            subject_qty_g=120,
            subject_qty_unit="kg"
        )

        # Create an empty instance;
        snr = model.nutrients.SettableNutrientRatio(nutrient_name="tirbur", subject=mock.Mock())

        # Assert the instance is undefined;
        self.assertFalse(snr.ratio_is_defined)

        # Load the data;
        snr.load_data(data)

        # Assert the data was loaded correctly;
        self.assertEqual(data, snr.persistable_data)
