from unittest import TestCase, mock

import model
from tests.model.nutrients import fixtures as fx
from tests.model.quantity import fixtures as qfx


class TestConstructor(TestCase):
    @fx.use_test_nutrients
    def test_can_construct_instance(self):
        snr = model.nutrients.SettableNutrientRatio(nutrient_name="tirbur", subject=mock.Mock())
        self.assertTrue(isinstance(snr, model.nutrients.SettableNutrientRatio))

    @fx.use_test_nutrients
    def test_loads_data_if_provided(self):
        snr = model.nutrients.SettableNutrientRatio(
            nutrient_name="tirbur",
            subject=mock.Mock(),
            nutrient_ratio_data=fx.init_nutrient_ratio_data(
                nutrient_qty_g=0.012, nutrient_pref_unit="mg",
                subject_qty_g=120, subject_pref_unit="kg"
            )
        )
        self.assertEqual(0.012, snr.nutrient_mass.quantity_in_g)
        self.assertEqual("mg", snr.nutrient_mass.pref_unit)
        self.assertEqual(120, snr.subject_ref_quantity.quantity_in_g)
        self.assertEqual("kg", snr.subject_ref_quantity.pref_unit)


class TestSetRatio(TestCase):
    @fx.use_test_nutrients
    def test_valid_data_is_set_correctly(self):
        snr = model.nutrients.SettableNutrientRatio(
            nutrient_name="tirbur",
            subject=qfx.SupportsExtendedUnitsTestable(g_per_ml=1.1)
        )
        snr.set_ratio(
            nutrient_mass=12,
            nutrient_mass_unit="mg",
            subject_qty=0.1,
            subject_qty_unit="kg"
        )
        self.assertEqual(0.012, snr.nutrient_mass.quantity_in_g)
        self.assertEqual("mg", snr.nutrient_mass.pref_unit)
        self.assertEqual(100, snr.subject_ref_quantity.quantity_in_g)
        self.assertEqual("kg", snr.subject_ref_quantity.pref_unit)

    @fx.use_test_nutrients
    def test_subject_qty_can_be_volume_if_configured(self):
        snr = model.nutrients.SettableNutrientRatio(
            nutrient_name="tirbur",
            subject=qfx.SupportsExtendedUnitsTestable(g_per_ml=1.5)
        )
        snr.set_ratio(
            nutrient_mass=12,
            nutrient_mass_unit="mg",
            subject_qty=0.5,
            subject_qty_unit="L"
        )
        self.assertEqual(0.012, snr.nutrient_mass.quantity_in_g)
        self.assertEqual("mg", snr.nutrient_mass.pref_unit)
        self.assertEqual(750, snr.subject_ref_quantity.quantity_in_g)
        self.assertEqual("l", snr.subject_ref_quantity.pref_unit)

    @fx.use_test_nutrients
    def test_exception_if_subject_qty_is_volume_and_not_configured(self):
        snr = model.nutrients.SettableNutrientRatio(
            nutrient_name="tirbur",
            subject=qfx.SupportsExtendedUnitsTestable(g_per_ml=None)
        )
        with self.assertRaises(model.quantity.exceptions.UndefinedDensityError):
            snr.set_ratio(
                nutrient_mass=12,
                nutrient_mass_unit="mg",
                subject_qty=0.5,
                subject_qty_unit="L"
            )

    @fx.use_test_nutrients
    def test_exception_if_nutrient_mass_unit_is_not_a_mass(self):
        snr = model.nutrients.SettableNutrientRatio(
            nutrient_name="tirbur",
            subject=qfx.SupportsExtendedUnitsTestable(g_per_ml=1.1)
        )
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
    @fx.use_test_nutrients
    def test_nutrient_ratio_undefined_correctly(self):
        snr = model.nutrients.SettableNutrientRatio(
            nutrient_name="tirbur",
            subject=qfx.SupportsExtendedUnitsTestable(g_per_ml=1.1)
        )
        snr.set_ratio(
            nutrient_mass=12,
            nutrient_mass_unit="mg",
            subject_qty=0.1,
            subject_qty_unit="kg"
        )
        self.assertTrue(snr.is_defined)
        snr.undefine()
        self.assertFalse(snr.is_defined)


class TestZero(TestCase):
    @fx.use_test_nutrients
    def test_nutrient_ratio_zeroed_correctly(self):
        snr = model.nutrients.SettableNutrientRatio(
            nutrient_name="tirbur",
            subject=qfx.SupportsExtendedUnitsTestable(g_per_ml=1.1)
        )
        snr.set_ratio(
            nutrient_mass=12,
            nutrient_mass_unit="mg",
            subject_qty=0.1,
            subject_qty_unit="kg"
        )
        self.assertEqual(0.012, snr.nutrient_mass.quantity_in_g)
        snr.zero()
        self.assertEqual(0, snr.nutrient_mass.quantity_in_g)
        self.assertTrue(snr.is_zero)


class TestLoadData(TestCase):
    @fx.use_test_nutrients
    def test_load_data(self):
        snr = model.nutrients.SettableNutrientRatio(nutrient_name="tirbur", subject=mock.Mock())
        self.assertEqual(
            fx.init_nutrient_ratio_data(),
            snr.persistable_data
        )
        snr.load_data(fx.init_nutrient_ratio_data(nutrient_qty_g=0.5, nutrient_pref_unit="mg",
                                                  subject_qty_g=1.2, subject_pref_unit="kg"))
        self.assertEqual(
            fx.init_nutrient_ratio_data(nutrient_qty_g=0.5, nutrient_pref_unit="mg",
                                        subject_qty_g=1.2, subject_pref_unit="kg"),
            snr.persistable_data
        )
