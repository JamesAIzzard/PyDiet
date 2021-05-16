from unittest import TestCase, mock

import model
from tests.model.nutrients import fixtures as fx
from tests.model.quantity import fixtures as q_fx


class TestConstructor(TestCase):
    @fx.use_test_nutrients
    def test_can_instantiate(self):
        nr = model.nutrients.NutrientRatio(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            nutrient_ratio_data_src=lambda: model.nutrients.NutrientRatioData(
                nutrient_mass_data=model.quantity.QuantityData(
                    quantity_in_g=0.012,
                    pref_unit="mg"
                ),
                subject_ref_qty_data=model.quantity.QuantityData(
                    quantity_in_g=100,
                    pref_unit='g'
                )
            )
        )
        self.assertTrue(isinstance(nr, model.nutrients.NutrientRatio))


class TestSubject(TestCase):
    @fx.use_test_nutrients
    def test_returns_subject_correctly(self):
        subject = mock.Mock()
        nr = fx.init_nutrient_ratio(subject=subject, nutrient_name="tirbur", data_src=mock.Mock())
        self.assertTrue(subject is nr.subject)


class TestNutrientMass(TestCase):
    @fx.use_test_nutrients
    def test_returns_nutrient_mass_instance(self):
        nr = fx.init_nutrient_ratio(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            data_src=fx.init_nutrient_ratio_data_src()
        )
        self.assertTrue(isinstance(nr.nutrient_mass, model.nutrients.NutrientMass))

    @fx.use_test_nutrients
    def test_nutrient_mass_has_correct_value(self):
        nr = fx.init_nutrient_ratio(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            data_src=fx.init_nutrient_ratio_data_src(nutrient_qty_g=12, subject_qty_g=100)
        )
        self.assertEqual(12, nr.nutrient_mass.quantity_in_g)

    @fx.use_test_nutrients
    def test_nutrient_mass_has_correct_pref_unit(self):
        nr = fx.init_nutrient_ratio(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            data_src=fx.init_nutrient_ratio_data_src(nutrient_qty_g=12, nutrient_pref_unit="mg", subject_qty_g=100)
        )
        self.assertEqual("mg", nr.nutrient_mass.pref_unit)

    @fx.use_test_nutrients
    def test_nutrient_mass_has_correct_ref_qty(self):
        nr = fx.init_nutrient_ratio(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            data_src=fx.init_nutrient_ratio_data_src(nutrient_qty_g=0.012, nutrient_pref_unit="mg", subject_qty_g=100)
        )
        self.assertEqual(12, nr.nutrient_mass.ref_qty)


class TestNutrientName(TestCase):
    @fx.use_test_nutrients
    def test_nutrient_name_is_correct(self):
        nr = fx.init_nutrient_ratio(subject=mock.Mock(), nutrient_name="tirbur", data_src=mock.Mock())
        self.assertEqual("tirbur", nr.nutrient_name)


class TestSubjectRefQty(TestCase):
    @fx.use_test_nutrients
    def test_correct_qty_g_is_returned(self):
        nr = fx.init_nutrient_ratio(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            data_src=fx.init_nutrient_ratio_data_src(nutrient_qty_g=12, nutrient_pref_unit="mg",
                                                     subject_qty_g=120, subject_pref_unit="lb")
        )
        self.assertEqual(120, nr.subject_ref_quantity.quantity_in_g)

    @fx.use_test_nutrients
    def test_correct_pref_unit_is_returned(self):
        nr = fx.init_nutrient_ratio(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            data_src=fx.init_nutrient_ratio_data_src(nutrient_qty_g=12, nutrient_pref_unit="mg",
                                                     subject_qty_g=120, subject_pref_unit="lb")
        )
        self.assertEqual("lb", nr.subject_ref_quantity.pref_unit)

    @fx.use_test_nutrients
    def test_correct_ref_qty_is_returned(self):
        nr = fx.init_nutrient_ratio(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            data_src=fx.init_nutrient_ratio_data_src(nutrient_qty_g=12, nutrient_pref_unit="mg",
                                                     subject_qty_g=120, subject_pref_unit="lb")
        )
        self.assertAlmostEqual(0.2624, nr.subject_ref_quantity.ref_qty, delta=0.01)

    @fx.use_test_nutrients
    def test_raises_exception_if_subject_tries_to_return_volume_when_density_not_configured(self):
        nr = fx.init_nutrient_ratio(
            subject=q_fx.get_subject_with_density(g_per_ml=None),
            nutrient_name="tirbur",
            data_src=fx.init_nutrient_ratio_data_src(nutrient_qty_g=12, nutrient_pref_unit="mg",
                                                     subject_qty_g=1.2, subject_pref_unit="L")
        )
        with self.assertRaises(model.quantity.exceptions.UndefinedDensityError):
            self.assertAlmostEqual(0.2624, nr.subject_ref_quantity.ref_qty, delta=0.01)


class TestGPerSubjectG(TestCase):
    @fx.use_test_nutrients
    def test_g_per_subject_g_is_correct_when_non_zero(self):
        nr = fx.init_nutrient_ratio(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            data_src=fx.init_nutrient_ratio_data_src(nutrient_qty_g=12, nutrient_pref_unit="mg",
                                                     subject_qty_g=120, subject_pref_unit="lb")
        )
        self.assertEqual(0.1, nr.g_per_subject_g)

    @fx.use_test_nutrients
    def test_g_per_subject_g_is_correct_when_zero(self):
        nr = fx.init_nutrient_ratio(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            data_src=fx.init_nutrient_ratio_data_src(nutrient_qty_g=0, nutrient_pref_unit="mg",
                                                     subject_qty_g=100, subject_pref_unit="g")
        )
        self.assertEqual(0, nr.g_per_subject_g)

    @fx.use_test_nutrients
    def test_raises_exception_if_nutrient_mass_is_not_defined(self):
        nr = fx.init_nutrient_ratio(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            data_src=fx.init_nutrient_ratio_data_src(nutrient_qty_g=None, nutrient_pref_unit="mg",
                                                     subject_qty_g=None, subject_pref_unit="lb")
        )
        with self.assertRaises(model.nutrients.exceptions.UndefinedNutrientRatioError):
            _ = nr.g_per_subject_g


class TestMassInNutrientPrefUnitPerSubjectG(TestCase):
    @fx.use_test_nutrients
    def test_correct_value_is_returned(self):
        nr = fx.init_nutrient_ratio(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            data_src=fx.init_nutrient_ratio_data_src(nutrient_qty_g=0.012, nutrient_pref_unit="mg",
                                                     subject_qty_g=100, subject_pref_unit="g")
        )
        self.assertAlmostEqual(0.12, nr.mass_in_nutrient_pref_unit_per_subject_g, delta=0.001)


class TestMassInNutrientPrefUnitPerSubjectReqQty(TestCase):
    @fx.use_test_nutrients
    def test_correct_value_is_returned(self):
        nr = fx.init_nutrient_ratio(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            data_src=fx.init_nutrient_ratio_data_src(nutrient_qty_g=0.012, nutrient_pref_unit="mg",
                                                     subject_qty_g=100, subject_pref_unit="g")
        )
        self.assertAlmostEqual(12, nr.mass_in_nutrient_pref_unit_per_subject_ref_qty, delta=0.001)


class TestIsDefined(TestCase):
    @fx.use_test_nutrients
    def test_returns_true_if_nutrient_ratio_defined(self):
        nr = fx.init_nutrient_ratio(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            data_src=fx.init_nutrient_ratio_data_src(nutrient_qty_g=0.012, nutrient_pref_unit="mg",
                                                     subject_qty_g=100, subject_pref_unit="g")
        )
        self.assertTrue(nr.is_defined)

    @fx.use_test_nutrients
    def test_returns_false_if_nutrient_ratio_not_defined(self):
        nr = fx.init_nutrient_ratio(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            data_src=fx.init_nutrient_ratio_data_src(nutrient_qty_g=None, nutrient_pref_unit="g",
                                                     subject_qty_g=100, subject_pref_unit="g")
        )
        self.assertFalse(nr.is_defined)


class TestIsZero(TestCase):
    @fx.use_test_nutrients
    def test_returns_true_if_nutrient_zero(self):
        nr = fx.init_nutrient_ratio(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            data_src=fx.init_nutrient_ratio_data_src(nutrient_qty_g=0, nutrient_pref_unit="g",
                                                     subject_qty_g=100, subject_pref_unit="g")
        )
        self.assertTrue(nr.is_zero)

    @fx.use_test_nutrients
    def test_returns_false_if_nutrient_not_zero(self):
        nr = fx.init_nutrient_ratio(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            data_src=fx.init_nutrient_ratio_data_src(nutrient_qty_g=10, nutrient_pref_unit="g",
                                                     subject_qty_g=100, subject_pref_unit="g")
        )
        self.assertFalse(nr.is_zero)


class TestIsNonZero(TestCase):
    @fx.use_test_nutrients
    def test_returns_false_if_nutrient_zero(self):
        nr = fx.init_nutrient_ratio(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            data_src=fx.init_nutrient_ratio_data_src(nutrient_qty_g=0, nutrient_pref_unit="g",
                                                     subject_qty_g=100, subject_pref_unit="g")
        )
        self.assertFalse(nr.is_non_zero)

    @fx.use_test_nutrients
    def test_returns_true_if_nutrient_not_zero(self):
        nr = fx.init_nutrient_ratio(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            data_src=fx.init_nutrient_ratio_data_src(nutrient_qty_g=10, nutrient_pref_unit="g",
                                                     subject_qty_g=100, subject_pref_unit="g")
        )
        self.assertTrue(nr.is_non_zero)


class TestPersistableData(TestCase):
    @fx.use_test_nutrients
    def test_returns_correct_data(self):
        nr = fx.init_nutrient_ratio(
            subject=mock.Mock(),
            nutrient_name="tirbur",
            data_src=fx.init_nutrient_ratio_data_src(nutrient_qty_g=0.5, nutrient_pref_unit="mg",
                                                     subject_qty_g=1, subject_pref_unit="kg")
        )
        self.assertEqual(
            model.nutrients.NutrientRatioData(
                nutrient_mass_data=model.quantity.QuantityData(
                    quantity_in_g=0.5,
                    pref_unit="mg"
                ),
                subject_ref_qty_data=model.quantity.QuantityData(
                    quantity_in_g=1,
                    pref_unit='kg'
                )
            ),
            nr.persistable_data
        )
