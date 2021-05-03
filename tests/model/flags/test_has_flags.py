from unittest import TestCase, mock

import model
import tests.model.nutrients.fixtures as nut_fx
from tests.model.flags import fixtures as fx


class TestConstructor(TestCase):
    def test_makes_correct_instance(self):
        hf = fx.HasFlagsTestable()
        self.assertTrue(isinstance(hf, model.flags.HasFlags))


class TestGetFlagDOF(TestCase):
    def setUp(self) -> None:
        self.flag_dofs = {
            "pongaterian": True,
            "foogetarian": False,
            "bar_free": None
        }

    @fx.use_test_flags
    def test_gets_dof_correctly(self):
        hf = fx.HasFlagsTestable(flag_dofs=self.flag_dofs)
        self.assertTrue(hf._get_flag_dof("pongaterian"))
        self.assertFalse(hf._get_flag_dof("foogetarian"))
        self.assertEqual(hf._get_flag_dof("bar_free"), None)

    @fx.use_test_flags
    def test_raises_exception_if_flag_has_no_dof(self):
        hf = fx.HasFlagsTestable()
        with self.assertRaises(model.flags.exceptions.FlagHasNoDOFError):
            _ = hf._get_flag_dof("foo_free")

    @fx.use_test_flags
    def test_returns_none_if_dof_not_listed(self):
        hf = fx.HasFlagsTestable(flag_dofs={})
        self.assertEqual(hf._get_flag_dof("pongaterian"), None)


class TestGatherAllRelatedNutrientRatios(TestCase):
    def setUp(self):
        self.nutrient_ratios = {
            "foo": mock.Mock(),
            "foobing": mock.Mock(),
            "foobar": mock.Mock(),
            "bar": mock.Mock(),
            "ping": mock.Mock()
        }

    @fx.use_test_flags
    @nut_fx.use_test_nutrients
    def test_correct_nutrient_ratios_returned(self):
        hf = fx.HasFlagsTestable(nutrient_ratios=self.nutrient_ratios)
        # Check the right nutrient ratios get returned;
        self.assertEqual(
            hf.gather_all_related_nutrient_ratios("foo_free"),
            [
                self.nutrient_ratios["foo"],
                self.nutrient_ratios["foobing"],
                self.nutrient_ratios["foobar"]
            ]
        )

    @fx.use_test_flags
    @nut_fx.use_test_nutrients
    def test_empty_list_returned_if_instance_has_no_related_nutrient_ratios(self):
        hf = fx.HasFlagsTestable()
        self.assertEqual(hf.gather_all_related_nutrient_ratios("pongaterian"), [])

    @fx.use_test_flags
    @nut_fx.use_test_nutrients
    def test_empty_list_if_flag_has_no_related_nutrients(self):
        hf = fx.HasFlagsTestable()
        self.assertEqual(hf.gather_all_related_nutrient_ratios("bar_free"), [])


class TestGetFlagValue(TestCase):
    @fx.use_test_flags
    def test_dof_used_when_set_flag_has_no_related_nutrients(self):
        hf = fx.HasFlagsTestable(flag_dofs={"foogetarian": True})
        self.assertTrue(hf.get_flag_value("foogetarian"))
        hf = fx.HasFlagsTestable(flag_dofs={"foogetarian": False})
        self.assertFalse(hf.get_flag_value("foogetarian"))
