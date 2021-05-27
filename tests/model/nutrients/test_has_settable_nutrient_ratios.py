"""Tests for the HasSettableNutrientRatios base class."""
from unittest import TestCase, mock

import model
from tests.model.nutrients import fixtures as fx


class TestConstructor(TestCase):
    """This is an early test to make sure:
    1. We can init the class without errors, i.e the constructor isn't broken.
    2. Any data provided to the constructor ends up in the instance.
    """

    def test_can_construct_instance(self):
        """Check we can construct the instance without errors."""
        hsnr = model.nutrients.HasSettableNutrientRatios()  # noqa - Suppress unused var warning.

    def test_any_data_provided_gets_loaded(self):
        """Check that any data we send in to the constructor actually ends up on the instance."""
        # Generate some dummy data;
        nr_data = mock.Mock()

        # Mock out the load_data method so we can check it got called;
        with mock.patch('model.nutrients.HasSettableNutrientRatios.load_data', mock.Mock()) as mk_load_data:
            # Pass the dummy data in when we spin up the instance;
            _ = model.nutrients.HasSettableNutrientRatios(nutrient_ratios_data=nr_data)

            # Now check that load data was called;
            # Notice how load expects the data to be under its specific heading in the dict;
            mk_load_data.assert_called_once_with({"nutrient_ratios_data": nr_data})


class TestNutrientRatios(TestCase):
    """Test the nutrient_ratios property."""

    @fx.use_test_nutrients
    def test_returns_correct_keys(self):
        """Checks that we have a key in the dict for each nutrient ratio which is defined
        on the instance."""
        # Create a test instance with some nr data;
        hsnr = model.nutrients.HasSettableNutrientRatios(nutrient_ratios_data={
            "regatur": fx.get_nutrient_ratio_data(nutrient_mass_g=12, subject_qty_g=100),
            "fillydon": fx.get_nutrient_ratio_data(nutrient_mass_g=12, subject_qty_g=100)
        })

        # Check the right keys show up in the dictionary;
        self.assertEqual(
            {"regatur", "fillydon"},
            set(hsnr.nutrient_ratios.keys())
        )

    @fx.use_test_nutrients
    def test_returns_readonly_nutrient_ratios(self):
        """Checks that we are not returning writable versions which could be given out and modified
        out of context of the subject."""
        # Create a test instance with some nr data;
        hsnr = model.nutrients.HasSettableNutrientRatios(nutrient_ratios_data={
            "regatur": fx.get_nutrient_ratio_data(nutrient_mass_g=12, subject_qty_g=100),
            "fillydon": fx.get_nutrient_ratio_data(nutrient_mass_g=12, subject_qty_g=100)
        })

        # Check the instances are the right type;
        for nutrient_ratio in hsnr.nutrient_ratios.values():
            self.assertTrue(isinstance(nutrient_ratio, model.nutrients.NutrientRatio))
            self.assertFalse(isinstance(nutrient_ratio, model.nutrients.SettableNutrientRatio))


class TestGetSettableNutrientRatio(TestCase):
    """This is the internal method which provides lookup functionality to return SettableNutrientRatio
    instances to be used internally."""

    @fx.use_test_nutrients
    def test_returns_correct_data(self):
        """Check that we get the nutrient ratio corresponding to the nutrient we asked for."""
        # Create a test instance with some nr data;
        hsnr = model.nutrients.HasSettableNutrientRatios(nutrient_ratios_data={
            "regatur": fx.get_nutrient_ratio_data(
                nutrient_mass_g=12,
                nutrient_mass_unit="mg",
                subject_qty_g=100,
                subject_qty_unit="kg"
            ),
            "fillydon": fx.get_nutrient_ratio_data(
                nutrient_mass_g=14,
                nutrient_mass_unit="g",
                subject_qty_g=120,
                subject_qty_unit="g"
            )
        })

        # Check we get the isntance we asked for;
        self.assertEqual(12, hsnr._get_settable_nutrient_ratio(nutrient_name="regatur").nutrient_mass.quantity_in_g)
        self.assertEqual("mg", hsnr._get_settable_nutrient_ratio(nutrient_name="regatur").nutrient_mass.pref_unit)
        self.assertEqual(
            100, hsnr._get_settable_nutrient_ratio(nutrient_name="regatur").subject_ref_quantity.quantity_in_g
        )
        self.assertEqual(
            "kg", hsnr._get_settable_nutrient_ratio(nutrient_name="regatur").subject_ref_quantity.pref_unit
        )

    @fx.use_test_nutrients
    def test_returns_writeable_instance(self):
        """Check that the instance we get back is actually a writable version."""
        # Create a test instance with some nr data;
        hsnr = model.nutrients.HasSettableNutrientRatios(nutrient_ratios_data={
            "regatur": fx.get_nutrient_ratio_data(nutrient_mass_g=12, subject_qty_g=100),
            "fillydon": fx.get_nutrient_ratio_data(nutrient_mass_g=12, subject_qty_g=100)
        })

        # Check we get the correct type of instance back;
        self.assertTrue(isinstance(
            hsnr._get_settable_nutrient_ratio("regatur"),
            model.nutrients.SettableNutrientRatio
        ))

    @fx.use_test_nutrients
    def test_raises_exception_if_nutrient_ratio_no_defined(self):
        """Check that we get an UndefinedNutrientRatioError if the nutrient ratio we ask for isnt defined."""
        hsnr = model.nutrients.HasSettableNutrientRatios()
        with self.assertRaises(model.nutrients.exceptions.UndefinedNutrientRatioError):
            _ = hsnr._get_settable_nutrient_ratio("foo")


class TestSetNutrientRatio(TestCase):
    """This is the public method responsible for setting a nutrient ratio on the instance. Therefore,
    the method is responsible for validating the new values within the context of the existing values."""

    @fx.use_test_nutrients
    def test_sets_nutrient_ratio_which_was_previously_unset_correctly(self):
        """Check that we can set a nutrient ratio which was previously unset, without errors."""
        # Create the instance;
        hsnr = model.nutrients.HasSettableNutrientRatios()

        # Assert tirbur is unset;
        self.assertFalse(hsnr.nutrient_ratio_is_defined("tirbur"))

        # Set the ratio;
        hsnr.set_nutrient_ratio(
            nutrient_name="tirbur",
            nutrient_mass=20,
            nutrient_mass_unit="ug",
            subject_qty=0.5,
            subject_qty_unit="lb"
        )

        # Now verify that all the data is as it should be;
        tb = hsnr.get_nutrient_ratio("tirbur")
        self.assertTrue(tb.subject_ref_quantity.subject is hsnr)
        self.assertAlmostEqual(2e-6, tb.nutrient_mass.quantity_in_g, delta=0.01)
        self.assertEqual("ug", tb.nutrient_mass.pref_unit)
        self.assertAlmostEqual(226.796, tb.subject_ref_quantity.quantity_in_g, delta=0.01)
        self.assertEqual("lb", tb.subject_ref_quantity.pref_unit)

    @fx.use_test_nutrients
    def test_sets_nutrient_ratio_which_was_previously_set_correctly(self):
        """Check that we can set a nutrient ratio which was previously set, without errors."""
        # Create a test instance with some nr data;
        hsnr = model.nutrients.HasSettableNutrientRatios(nutrient_ratios_data={
            "regatur": fx.get_nutrient_ratio_data(nutrient_mass_g=12, subject_qty_g=100),
            "fillydon": fx.get_nutrient_ratio_data(nutrient_mass_g=12, subject_qty_g=100)
        })

        # Assert the nutrient is set already;
        self.assertTrue(hsnr.nutrient_ratio_is_defined("regatur"))

        # Set the ratio;
        hsnr.set_nutrient_ratio(
            nutrient_name="regatur",
            nutrient_mass=20,
            nutrient_mass_unit="g",
            subject_qty=100,
            subject_qty_unit="g"
        )

        # Now verify that all the data is as it should be;
        tb = hsnr.get_nutrient_ratio("regatur")
        self.assertTrue(tb.subject_ref_quantity.subject is hsnr)
        self.assertAlmostEqual(20, tb.nutrient_mass.quantity_in_g, delta=0.01)
        self.assertEqual("g", tb.nutrient_mass.pref_unit)
        self.assertAlmostEqual(100, tb.subject_ref_quantity.quantity_in_g, delta=0.01)
        self.assertEqual("g", tb.subject_ref_quantity.pref_unit)

    @fx.use_test_nutrients
    def test_sets_nutrient_ratio_using_subject_volume_when_density_is_defined(self):
        """Check that we can set a nutrient ratio using a volume unit provided when the
        subject density is defined. Strictly, this functionality mostly belongs to the
        quantity classes, but it is useful to do a integrated test here. """
        # Create the instance;
        hsnr = fx.HasSettableNutrientRatiosAndExtUnitsTestable(g_per_ml=1.1)

        # Set the ratio;
        hsnr.set_nutrient_ratio(
            nutrient_name="tirbur",
            nutrient_mass=20,
            nutrient_mass_unit="ug",
            subject_qty=0.5,
            subject_qty_unit="l"
        )

        # Now verify that all the data is as it should be;
        tb = hsnr.get_nutrient_ratio("tirbur")
        self.assertTrue(tb.subject_ref_quantity.subject is hsnr)
        self.assertAlmostEqual(2e-6, tb.nutrient_mass.quantity_in_g, delta=0.01)
        self.assertEqual("ug", tb.nutrient_mass.pref_unit)
        self.assertAlmostEqual(550, tb.subject_ref_quantity.quantity_in_g, delta=0.01)
        self.assertEqual("l", tb.subject_ref_quantity.pref_unit)

    @fx.use_test_nutrients
    def test_raises_exception_if_unsupported_extended_units_are_used(self):
        """Check that we get an unsupported units exception if we try and use extended units on
        a class that doesn't support them. Again, this overlaps with validation done in the
        quantity module, but worth doing an integrated test."""

        # Create the instance;
        hsnr = model.nutrients.HasSettableNutrientRatios()

        # Check we get the exception when we try and set the ratio;
        with self.assertRaises(model.quantity.exceptions.UnsupportedExtendedUnitsError):
            hsnr.set_nutrient_ratio(
                nutrient_name="tirbur",
                nutrient_mass=20,
                nutrient_mass_unit="ug",
                subject_qty=0.5,
                subject_qty_unit="l"
            )

    @fx.use_test_nutrients
    def test_sets_nutrient_ratio_using_subject_volume_when_density_is_defined(self):
        """Check that using extended units on the subject, when the subject does support them
        but they are undefined, raises the right exception. Integrated version of functionality
        also tested on the quantity module."""

        # Create the instance;
        hsnr = fx.HasSettableNutrientRatiosAndExtUnitsTestable(g_per_ml=None)

        # Check we get the right exception when we try to set the ratio;
        with self.assertRaises(model.quantity.exceptions.UndefinedDensityError):
            hsnr.set_nutrient_ratio(
                nutrient_name="tirbur",
                nutrient_mass=20,
                nutrient_mass_unit="ug",
                subject_qty=0.5,
                subject_qty_unit="l"
            )

    def test_raises_exception_if_nutrient_name_not_recognised(self):
        """Check we get an exception if we try to set a nutrient ratio for a nutrient whose
        name is not recognised."""
        # Create the instance;
        hsnr = model.nutrients.HasSettableNutrientRatios()

        # Check for the exception;
        with self.assertRaises(model.nutrients.exceptions.NutrientNameNotRecognisedError):
            hsnr.set_nutrient_ratio(
                nutrient_name="fake",
                nutrient_mass=20,
                nutrient_mass_unit="ug",
                subject_qty=0.5,
                subject_qty_unit="l"
            )

    @fx.use_test_nutrients
    def test_raises_exception_if_nutrient_qty_exceeds_subject_qty(self):
        """Checks that we get an exception if we try to set the nutrient quantity greater than
        the subject quantity."""
        # Create the instance;
        hsnr = model.nutrients.HasSettableNutrientRatios()

        # Check we get the right exception when we try to set the ratio;
        with self.assertRaises(model.nutrients.exceptions.NutrientQtyExceedsSubjectQtyError):
            hsnr.set_nutrient_ratio(
                nutrient_name="tirbur",
                nutrient_mass=10000,  # 10g
                nutrient_mass_unit="mg",
                subject_qty=9,
                subject_qty_unit="g"
            )

    @fx.use_test_nutrients
    def test_raises_exception_if_nutrient_qty_is_not_mass(self):
        """Checks we get an exception if the nutrient quantity is not a mass. This is an integrated test,
        primarily relying on validation done in the NutrientMass class."""
        # Create the instance;
        hsnr = model.nutrients.HasSettableNutrientRatios()

        # Check we get the right exception when we try to set the ratio;
        with self.assertRaises(model.quantity.exceptions.UnsupportedExtendedUnitsError):
            hsnr.set_nutrient_ratio(
                nutrient_name="tirbur",
                nutrient_mass=10,
                nutrient_mass_unit="ml",
                subject_qty=100,
                subject_qty_unit="g"
            )

    @fx.use_test_nutrients
    def test_raises_exception_if_nutrient_is_set_for_zero_subject_quantity(self):
        """This checks that we get a zero qty error if we try and set a nutrient ratio against
        a zero subject quantity, which obviously doesn't make sense."""

        # Create the instance;
        hsnr = model.nutrients.HasSettableNutrientRatios()

        # Check we get the right exception when we try to set the ratio;
        with self.assertRaises(model.quantity.exceptions.ZeroQtyError):
            hsnr.set_nutrient_ratio(
                nutrient_name="tirbur",
                nutrient_mass=10,
                nutrient_mass_unit="ml",
                subject_qty=0,
                subject_qty_unit="g"
            )


class TestUndefineNutrientRatio(TestCase):
    @fx.use_test_nutrients
    def test_nutrient_ratio_is_undefined(self):
        """Checks that the named nutrient ratio is undefined correctly."""
        # Create a test instance with some nr data;
        hsnr = model.nutrients.HasSettableNutrientRatios(nutrient_ratios_data={
            "regatur": fx.get_nutrient_ratio_data(nutrient_mass_g=12, subject_qty_g=100),
            "fillydon": fx.get_nutrient_ratio_data(nutrient_mass_g=12, subject_qty_g=100)
        })

        # Assert that the nutrient is defined;
        self.assertTrue(hsnr.nutrient_ratio_is_defined("regatur"))

        # Undefine it;
        hsnr.undefine_nutrient_ratio("regatur")

        # Assert that the nutrient ratio is undefined;
        self.assertFalse(hsnr.nutrient_ratio_is_defined("regatur"))


class TestZeroNutrientRatio(TestCase):
    @fx.use_test_nutrients
    def test_nutrient_ratio_is_zeroed(self):
        """Checks that the named nutrient ratio is zeroed correctly."""
        # Create a test instance with some nr data;
        hsnr = model.nutrients.HasSettableNutrientRatios(nutrient_ratios_data={
            "regatur": fx.get_nutrient_ratio_data(nutrient_mass_g=12, subject_qty_g=100),
            "fillydon": fx.get_nutrient_ratio_data(nutrient_mass_g=12, subject_qty_g=100)
        })

        # Assert that the nutrient is defined;
        self.assertFalse(hsnr.get_nutrient_ratio("regatur").is_zero)

        # Undefine it;
        hsnr.zero_nutrient_ratio("regatur")

        # Assert that the nutrient ratio is undefined;
        self.assertTrue(hsnr.get_nutrient_ratio("regatur").is_zero)


class TestLoadData(TestCase):
    @fx.use_test_nutrients
    def test_data_is_loaded_correctly(self):
        """Checks the data is loaded correctly."""
        # Create some test data;
        data = {
            "cufmagif": fx.get_nutrient_ratio_data(
                nutrient_mass_g=12,
                nutrient_mass_unit="mg",
                subject_qty_g=100,
                subject_qty_unit="kg"
            ),
            "tirbur": fx.get_nutrient_ratio_data(
                nutrient_mass_g=13,
                nutrient_mass_unit="ug",
                subject_qty_g=100,
                subject_qty_unit="L"
            ),
            "docbe": fx.get_nutrient_ratio_data(
                nutrient_mass_g=26,
                nutrient_mass_unit="g",
                subject_qty_g=100,
                subject_qty_unit="pc"
            )
        }

        # First we can create an instance without any data;
        hsnr = fx.HasSettableNutrientRatiosAndExtUnitsTestable(g_per_ml=1.2, piece_mass_g=120)

        # Assert that we have no data;
        self.assertTrue(len(hsnr.persistable_data['nutrient_ratios_data']) == 0)

        # Load the data;
        hsnr.load_data(data={'nutrient_ratios_data': data})

        # Assert the data was loaded correctly;
        self.assertEqual(3, len(hsnr.nutrient_ratios))
        self.assertEqual({"cufmagif", "tirbur", "docbe"}, set(hsnr.nutrient_ratios.keys()))
        self.assertEqual(12, hsnr.nutrient_ratios["cufmagif"].nutrient_mass.quantity_in_g)
        self.assertEqual(100, hsnr.nutrient_ratios["tirbur"].subject_ref_quantity.quantity_in_g)
        self.assertEqual('ug', hsnr.nutrient_ratios["tirbur"].nutrient_mass.pref_unit)
        self.assertEqual('pc', hsnr.nutrient_ratios["docbe"].subject_ref_quantity.pref_unit)

    @fx.use_test_nutrients
    def test_exception_if_data_contains_family_mass_error(self):
        """This checks we get an exception if we load data that contains family mass errors. This duplicates
        some tested functionality on the validation method, but it is useful to do as an integration test."""
        # Create an emtpy test instance;
        hsnr = fx.HasSettableNutrientRatiosAndExtUnitsTestable(g_per_ml=1.2, piece_mass_g=120)

        # Create some test data with an family mass error;
        data = {
            "cufmagif": fx.get_nutrient_ratio_data(
                nutrient_mass_g=12,
                nutrient_mass_unit="mg",
                subject_qty_g=100,
                subject_qty_unit="kg"
            ),
            "tirbur": fx.get_nutrient_ratio_data(
                nutrient_mass_g=13,
                nutrient_mass_unit="ug",
                subject_qty_g=100,
                subject_qty_unit="L"
            ),
            "docbe": fx.get_nutrient_ratio_data(
                nutrient_mass_g=24,
                nutrient_mass_unit="g",
                subject_qty_g=100,
                subject_qty_unit="pc"
            )
        }

        # Load the data, and assert we get an exception;
        with self.assertRaises(model.nutrients.exceptions.ChildNutrientExceedsParentMassError):
            hsnr.load_data(data={'nutrient_ratios_data': data})

    @fx.use_test_nutrients
    def test_exception_if_data_uses_unsupported_unit(self):
        """This checks we get an exception if we try to load data that uses units that are not supported."""
        # Create an instance that doesn't support ext units;
        hsnr = model.nutrients.HasSettableNutrientRatios()

        # Create some test data that uses ext units;
        data = {
            "cufmagif": fx.get_nutrient_ratio_data(
                nutrient_mass_g=12,
                nutrient_mass_unit="mg",
                subject_qty_g=100,
                subject_qty_unit="L"
            ),
        }

        # Load the data, and assert we get an exception;
        with self.assertRaises(model.quantity.exceptions.UnsupportedExtendedUnitsError):
            hsnr.load_data(data={'nutrient_ratios_data': data})

    @fx.use_test_nutrients
    def test_exception_if_data_uses_unconfigured_unit(self):
        """This checks we get an exception if we try to load data that uses units that are not configured."""
        # First we can create an instance without any data;
        hsnr = fx.HasSettableNutrientRatiosAndExtUnitsTestable(piece_mass_g=None)

        # Create some test data that uses ext units;
        data = {
            "cufmagif": fx.get_nutrient_ratio_data(
                nutrient_mass_g=12,
                nutrient_mass_unit="mg",
                subject_qty_g=100,
                subject_qty_unit="pc"
            ),
        }

        # Load the data, and assert we get an exception;
        with self.assertRaises(model.quantity.exceptions.UndefinedPcMassError):
            hsnr.load_data(data={'nutrient_ratios_data': data})
