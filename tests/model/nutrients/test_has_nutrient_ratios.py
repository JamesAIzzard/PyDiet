from unittest import TestCase, mock

import model
from tests.model.nutrients import fixtures as fx


class TestGetNutrientRatio(TestCase):
    @fx.use_test_nutrients
    def test_gets_nutrient_ratio_correctly(self):
        hnr = fx.HasNutrientRatiosTestable()
        hnr._nutrient_ratios = {
            "tirbur": mock.Mock(),
            "foo": mock.Mock(),
            "foobar": mock.Mock()
        }
        self.assertEqual(hnr._nutrient_ratios["foo"], hnr.get_nutrient_ratio("foo"))

    @fx.use_test_nutrients
    def test_raises_exception_if_nutrient_ratio_unset(self):
        hnr = fx.HasNutrientRatiosTestable()
        hnr._nutrient_ratios = {
            "tirbur": mock.Mock(),
            "foo": mock.Mock(),
            "foobar": mock.Mock()
        }
        with self.assertRaises(model.nutrients.exceptions.UndefinedNutrientRatioError):
            _ = hnr.get_nutrient_ratio("bazing")


class TestNutrientRatioIsDefined(TestCase):
    @fx.use_test_nutrients
    def test_returns_true_if_nutrient_ratio_defined(self):
        hnr = fx.HasNutrientRatiosTestable()
        hnr._nutrient_ratios = {
            "tirbur": mock.Mock(),
            "foo": mock.Mock(),
            "foobar": mock.Mock()
        }
        self.assertTrue(hnr.nutrient_ratio_is_defined("tirbur"))

    @fx.use_test_nutrients
    def test_returns_false_if_nutrient_ratio_undefined(self):
        hnr = fx.HasNutrientRatiosTestable()
        hnr._nutrient_ratios = {
            "tirbur": mock.Mock(),
            "foo": mock.Mock(),
            "foobar": mock.Mock()
        }
        self.assertFalse(hnr.nutrient_ratio_is_defined("docbe"))


class TestUndefinedMandatoryNutrientRatioNames(TestCase):
    @fx.use_test_nutrients
    def test_correctly_returns_undefined_mandatory_ratio_names(self):
        hnr = fx.HasNutrientRatiosTestable()
        hnr._nutrient_ratios = {
            "cufmagif": mock.Mock(),
            "foo": mock.Mock(),
            "foobar": mock.Mock()
        }
        self.assertEqual(
            {"bingtong", "regatur"},
            set(hnr.undefined_mandatory_nutrient_ratio_names)
        )


class TestDefinedOptionalNutrientRatioNames(TestCase):
    @fx.use_test_nutrients
    def test_correctly_returns_defined_optional_names(self):
        hnr = fx.HasNutrientRatiosTestable()
        hnr._nutrient_ratios = {
            "cufmagif": mock.Mock(),
            "foo": mock.Mock(),
            "foobar": mock.Mock()
        }
        self.assertEqual(
            {"foo", "foobar"},
            set(hnr.defined_optional_nutrient_ratio_names)
        )


class TestGetNutrientMassInPrefUnitPerSubjectRefQuantity(TestCase):
    @fx.use_test_nutrients
    def test_gets_correct_value(self):
        tirbur = mock.Mock()
        tirbur.mass_in_nutrient_pref_unit_per_subject_ref_qty = 12
        hnr = fx.HasNutrientRatiosTestable()
        hnr._nutrient_ratios = {
            "tirbur": tirbur,
            "foo": mock.Mock(),
            "foobar": mock.Mock()
        }
        self.assertEqual(12, hnr.get_nutrient_mass_in_pref_unit_per_subject_ref_qty("tirbur"))


class TestValidateNutrientRatio(TestCase):
    """The detailed testing of the validation method is done in testing.model.nutrients.test_main.
    Here, the aim is more to check that the custom getter function works, and raises the correct
    exceptions to allow the validator function to do its job. So we only do a couple of quick
    tests here, to check everything is spinning correctly.
    """

    @staticmethod
    def mock_nutrient_ratio(g_per_sub_g: float):
        m = mock.Mock()
        m.g_per_subject_g = g_per_sub_g
        return m

    @fx.use_test_nutrients
    def test_no_exception_if_no_error(self):
        hnr = fx.HasNutrientRatiosTestable()
        hnr._nutrient_ratios = {
            "cufmagif": self.mock_nutrient_ratio(0.3),
            "foo": self.mock_nutrient_ratio(0.4),
            "foobar": self.mock_nutrient_ratio(0.5)
        }
        hnr.validate_nutrient_ratio("cufmagif")

    @fx.use_test_nutrients
    def test_raises_exception_if_error(self):
        hnr = fx.HasNutrientRatiosTestable()
        hnr._nutrient_ratios = {
            "cufmagif": self.mock_nutrient_ratio(0.3),
            "bar": self.mock_nutrient_ratio(0.3),
            "foobar": self.mock_nutrient_ratio(0.3),
            "docbe": self.mock_nutrient_ratio(0.3),
        }
        with self.assertRaises(model.nutrients.exceptions.ChildNutrientExceedsParentMassError):
            hnr.validate_nutrient_ratio("cufmagif")


class TestPersistableData(TestCase):
    @fx.use_test_nutrients
    def test_data_dict_returned_correctly(self):
        """Checks that the persistable data dictionary is returned with the correct contents."""
        # Create the nutrient ratio instance;
        hnr = fx.HasSettableNutrientRatiosAndDensityTestable(g_per_ml=1.1, piece_mass_g=150)

        # Generate some nutrient data to pass through the instance;
        nutr_ratios = {
            "cufmagif": fx.init_nutrient_ratio(
                nutrient_name="cufmagif", subject=hnr,
                data_src=fx.init_nutrient_ratio_data_src(
                    nutrient_qty_g=12, nutrient_pref_unit="mg", subject_qty_g=200, subject_pref_unit="kg"
                )
            ),
            "tirbur": fx.init_nutrient_ratio(
                nutrient_name="tirbur", subject=hnr,
                data_src=fx.init_nutrient_ratio_data_src(
                    nutrient_qty_g=13, nutrient_pref_unit="ug", subject_qty_g=300, subject_pref_unit="L"
                )
            ),
            "docbe": fx.init_nutrient_ratio(
                nutrient_name="docbe", subject=hnr,
                data_src=fx.init_nutrient_ratio_data_src(
                    nutrient_qty_g=14, nutrient_pref_unit="g", subject_qty_g=400, subject_pref_unit="pc"
                )
            ),
        }

        # Put the data on the instance;
        hnr._nutrient_ratios = nutr_ratios

        # Specify what the output data should be;
        nutr_ratios_data = {
            "cufmagif": fx.init_nutrient_ratio_data(
                nutrient_qty_g=12, nutrient_pref_unit="mg", subject_qty_g=200, subject_pref_unit="kg"
            ),
            "tirbur": fx.init_nutrient_ratio_data(
                nutrient_qty_g=13, nutrient_pref_unit="ug", subject_qty_g=300, subject_pref_unit="L"
            ),
            "docbe": fx.init_nutrient_ratio_data(
                nutrient_qty_g=14, nutrient_pref_unit="g", subject_qty_g=400, subject_pref_unit="pc"
            )
        }

        # Now check that the peristable data we get out is the same as the nutrient data we passed in;
        self.assertEqual(nutr_ratios_data, hnr.persistable_data['nutrient_ratios_data'])
