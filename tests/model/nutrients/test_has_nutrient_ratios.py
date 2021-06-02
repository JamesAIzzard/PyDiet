"""Defines functionality related to nutrient ratios."""
from unittest import TestCase

import model
from tests.model.nutrients import fixtures as fx


class TestNutrientRatios(TestCase):
    """Tests the nutrient_ratios property."""

    @fx.use_test_nutrients
    def test_returns_test_nutrients_correctly(self):
        """Checks that we get the correct dict of readonly nutrient ratios."""
        # Create a test instance;
        hnr = fx.HasReadableNutrientRatiosTestable(nutrient_ratios_data={
            "foo": fx.get_nutrient_ratio_data(nutrient_mass_g=20, subject_qty_g=1, subject_qty_unit='kg'),
            "bar": fx.get_nutrient_ratio_data(nutrient_mass_g=30, nutrient_mass_unit='lb', subject_qty_g=140)
        })

        # Check we get the right number of nutrient ratios returned;
        self.assertEqual(2, len(hnr.nutrient_ratios))

        # Check that each nutrient ratio instance is the right type;
        for nr in hnr.nutrient_ratios.values():
            self.assertTrue(isinstance(nr, model.nutrients.ReadonlyNutrientRatio))

        # Check some of the values
        self.assertEqual(20, hnr.nutrient_ratios["foo"].nutrient_mass.quantity_in_g)
        self.assertEqual('kg', hnr.nutrient_ratios["foo"].subject_ref_quantity.qty_pref_unit)
        self.assertEqual(30, hnr.nutrient_ratios["bar"].nutrient_mass.quantity_in_g)
        self.assertEqual('lb', hnr.nutrient_ratios["bar"].nutrient_mass.qty_pref_unit)


class TestGetNutrientRatio(TestCase):
    """Tests the get_nutrient_ratio method."""

    @fx.use_test_nutrients
    def test_gets_nutrient_ratio_correctly(self):
        """Check that we can get the correct nutrient ratio instance by name."""
        # Create a test instance;
        hnr = fx.HasReadableNutrientRatiosTestable(nutrient_ratios_data={
            "tirbur": fx.get_nutrient_ratio_data(nutrient_mass_g=10, subject_qty_g=100),
            "foo": fx.get_nutrient_ratio_data(nutrient_mass_g=20, subject_qty_g=90)
        })

        # Check we get an instance of the correct type;
        foo = hnr.get_nutrient_ratio("foo")
        self.assertTrue(isinstance(foo, model.nutrients.ReadonlyNutrientRatio))

        # Check some of the details;
        self.assertEqual(20, foo.nutrient_mass.quantity_in_g)
        self.assertEqual(90, foo.subject_ref_quantity.quantity_in_g)

    @fx.use_test_nutrients
    def test_raises_exception_if_nutrient_ratio_unset(self):
        """Check that we get an exception if the nutrient ratio is unset;"""
        # Create a test instance;
        hnr = fx.HasReadableNutrientRatiosTestable(nutrient_ratios_data={
            "tirbur": fx.get_nutrient_ratio_data(nutrient_mass_g=10, subject_qty_g=100),
            "foo": fx.get_nutrient_ratio_data(nutrient_mass_g=20, subject_qty_g=90)
        })

        # Try to access one that isn't there, and assert we get an exception;
        with self.assertRaises(model.nutrients.exceptions.UndefinedNutrientRatioError):
            _ = hnr.get_nutrient_ratio("bazing")


class TestCaloriesPerG(TestCase):
    """Tests the calories_per_g property."""
    @fx.use_test_nutrients
    def test_returns_correct_value(self):
        """Checks the method returns the correct number of calories per gram."""
        # Create a test instance with some nutrient ratios with associated calories;
        hnr = fx.HasReadableNutrientRatiosTestable(nutrient_ratios_data={
            "tirbur": fx.get_nutrient_ratio_data(nutrient_mass_g=10, subject_qty_g=100),
            "regatur": fx.get_nutrient_ratio_data(nutrient_mass_g=10, subject_qty_g=100),
            "foo": fx.get_nutrient_ratio_data(nutrient_mass_g=20, subject_qty_g=100),
            "fillydon": fx.get_nutrient_ratio_data(nutrient_mass_g=30, subject_qty_g=100),
            "busskie": fx.get_nutrient_ratio_data(nutrient_mass_g=10, subject_qty_g=100),
            "bingtong": fx.get_nutrient_ratio_data(nutrient_mass_g=25, subject_qty_g=100)
        })

        # Assert we get the correct number of calories per gram;
        self.assertEqual(1.8, hnr.calories_per_g)

    @fx.use_test_nutrients
    def test_raises_exception_if_cal_nutrient_undefined(self):
        """Checks we get an exception if one of the nutrient calories is undefined."""
        # Create a test instance with some calorie nutrients undefined.
        hnr = fx.HasReadableNutrientRatiosTestable(nutrient_ratios_data={
            "tirbur": fx.get_nutrient_ratio_data(nutrient_mass_g=10, subject_qty_g=100),
            "regatur": fx.get_nutrient_ratio_data(nutrient_mass_g=10, subject_qty_g=100),
            "foo": fx.get_nutrient_ratio_data(nutrient_mass_g=20, subject_qty_g=100),
            "fillydon": fx.get_nutrient_ratio_data(nutrient_mass_g=30, subject_qty_g=100),
        })

        # Assert we get an exception if we try to access the property;
        with self.assertRaises(model.nutrients.exceptions.UndefinedCalorieNutrientRatioError):
            _ = hnr.calories_per_g


class TestNutrientRatioIsDefined(TestCase):
    """Tests the nutrient_ratio_is_defined property."""

    @fx.use_test_nutrients
    def test_returns_true_if_nutrient_ratio_defined(self):
        """Check that we get True if the nutrient ratio is defined."""
        # Create a test instance;
        hnr = fx.HasReadableNutrientRatiosTestable(nutrient_ratios_data={
            "tirbur": fx.get_nutrient_ratio_data(nutrient_mass_g=10, subject_qty_g=100),
            "foo": fx.get_nutrient_ratio_data(nutrient_mass_g=20, subject_qty_g=90)
        })

        # Check we get a True;
        self.assertTrue(hnr.nutrient_ratio_is_defined("tirbur"))

    @fx.use_test_nutrients
    def test_returns_false_if_nutrient_ratio_undefined(self):
        """Check we get a False if the nutrient ratio is undefined."""
        # Create a test instance;
        hnr = fx.HasReadableNutrientRatiosTestable(nutrient_ratios_data={
            "tirbur": fx.get_nutrient_ratio_data(nutrient_mass_g=10, subject_qty_g=100),
            "foo": fx.get_nutrient_ratio_data(nutrient_mass_g=20, subject_qty_g=90)
        })

        # Check we get a False;
        self.assertFalse(hnr.nutrient_ratio_is_defined("docbe"))


class TestUndefinedMandatoryNutrientRatioNames(TestCase):
    """Tests the mandatory nutrient ratio names are returned correctly;"""
    @fx.use_test_nutrients
    def test_correctly_returns_undefined_mandatory_ratio_names(self):
        # Create a test instance;
        hnr = fx.HasReadableNutrientRatiosTestable(nutrient_ratios_data={
            "cufmagif": fx.get_nutrient_ratio_data(nutrient_mass_g=10, subject_qty_g=100),
            "foo": fx.get_nutrient_ratio_data(nutrient_mass_g=20, subject_qty_g=90),
            "foobar": fx.get_nutrient_ratio_data(nutrient_mass_g=10, subject_qty_g=100)
        })

        # Check we get the correct names back;
        self.assertEqual(
            {"bingtong", "regatur"},
            set(hnr.undefined_mandatory_nutrient_ratio_names)
        )


class TestDefinedOptionalNutrientRatioNames(TestCase):
    @fx.use_test_nutrients
    def test_correctly_returns_defined_optional_names(self):
        """Check that we do get the defined optional nutrient names back."""
        # Create a test instnace;
        hnr = fx.HasReadableNutrientRatiosTestable(nutrient_ratios_data={
            "cufmagif": fx.get_nutrient_ratio_data(nutrient_mass_g=10, subject_qty_g=100),
            "foo": fx.get_nutrient_ratio_data(nutrient_mass_g=20, subject_qty_g=90),
            "foobar": fx.get_nutrient_ratio_data(nutrient_mass_g=10, subject_qty_g=100)
        })

        # Check the correct names are returned;
        self.assertEqual(
            {"foo", "foobar"},
            set(hnr.defined_optional_nutrient_ratio_names)
        )


class TestGetNutrientMassInPrefUnitPerSubjectRefQuantity(TestCase):
    """Tests for the get_nutrient_mass_in_pref_unit_per_subject_ref_qty method."""
    @fx.use_test_nutrients
    def test_gets_correct_value(self):
        """Check we get the correct value back."""

        # Create a test instance, with some test data;
        hnr = fx.HasReadableNutrientRatiosTestable({
            "tirbur": fx.get_nutrient_ratio_data(nutrient_mass_g=0.02, nutrient_mass_unit="mg",
                                                 subject_qty_g=150, subject_qty_unit="kg"),
            "foo": fx.get_nutrient_ratio_data(nutrient_mass_g=20, subject_qty_g=90),
            "foobar": fx.get_nutrient_ratio_data(nutrient_mass_g=10, subject_qty_g=100)
        })

        # Check we get 20mg per 0.15kg
        self.assertEqual(20, hnr.get_nutrient_mass_in_pref_unit_per_subject_ref_qty("tirbur"))


class TestValidateNutrientRatio(TestCase):
    """The detailed testing of the validation method is done in testing.model.nutrients.test_main.
    Here, the aim is more to check that the custom getter function works, and raises the correct
    exceptions to allow the validator function to do its job. So we only do a couple of quick
    tests here, to check everything is spinning correctly.
    """

    @fx.use_test_nutrients
    def test_no_exception_if_no_error(self):
        """Test we get no exception if there is no error."""
        hnr = fx.HasReadableNutrientRatiosTestable(nutrient_ratios_data={
            "cufmagif": fx.get_nutrient_ratio_data(nutrient_mass_g=0.3, subject_qty_g=1),
            "foo": fx.get_nutrient_ratio_data(nutrient_mass_g=0.4, subject_qty_g=1),
            "foobar": fx.get_nutrient_ratio_data(nutrient_mass_g=0.5, subject_qty_g=1)
        })

        # Check we get no error if we call the validation function.
        hnr.validate_nutrient_ratio("cufmagif")

    @fx.use_test_nutrients
    def test_raises_exception_if_error(self):
        """Checks that we do get an exception if there is an error."""
        hnr = fx.HasReadableNutrientRatiosTestable(nutrient_ratios_data={
            "cufmagif": fx.get_nutrient_ratio_data(nutrient_mass_g=0.3, subject_qty_g=1),
            "bar": fx.get_nutrient_ratio_data(nutrient_mass_g=0.3, subject_qty_g=1),
            "foobar": fx.get_nutrient_ratio_data(nutrient_mass_g=0.3, subject_qty_g=1),
            "docbe": fx.get_nutrient_ratio_data(nutrient_mass_g=0.3, subject_qty_g=1),
        })

        # Now check we get an exception, because cufmagif is a grandchid of docbe, along with bar,
        # so cufmagif and bar exceed the parent quantity.
        with self.assertRaises(model.nutrients.exceptions.ChildNutrientExceedsParentMassError):
            hnr.validate_nutrient_ratio("cufmagif")


class TestPersistableData(TestCase):
    @fx.use_test_nutrients
    def test_data_dict_returned_correctly(self):
        """Checks that the persistable data dictionary is returned with the correct contents."""
        # Create some test data;
        data = {
            "cufmagif": fx.get_nutrient_ratio_data(
                nutrient_mass_g=12,
                nutrient_mass_unit="mg",
                subject_qty_g=200,
                subject_qty_unit="kg"
            ),
            "tirbur": fx.get_nutrient_ratio_data(
                nutrient_mass_g=13,
                nutrient_mass_unit="ug",
                subject_qty_g=300,
                subject_qty_unit="L"
            ),
            "docbe": fx.get_nutrient_ratio_data(
                nutrient_mass_g=14,
                nutrient_mass_unit="g",
                subject_qty_g=400,
                subject_qty_unit="pc"
            )
        }

        # Create the nutrient ratio instance;
        hnr = fx.HasNutrientRatiosAndExtUnitsTestable(g_per_ml=1.1, piece_mass_g=150, nutrient_ratios_data=data)

        # Now check that the peristable data we get out is the same as the nutrient data we passed in;
        self.assertEqual(data, hnr.persistable_data['nutrient_ratios_data'])
