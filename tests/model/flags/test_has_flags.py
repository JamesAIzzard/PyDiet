from unittest import TestCase, mock

import model
import tests.model.flags
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

    @mock.patch.dict(model.flags.validation.ALL_FLAGS, tests.model.flags.ALL_TEST_FLAGS)
    @mock.patch.dict(model.flags.main.ALL_FLAGS, tests.model.flags.ALL_TEST_FLAGS)
    def test_gets_dof_correctly(self):
        hf = fx.HasFlagsTestable(flag_dofs=self.flag_dofs)
        self.assertTrue(hf._get_flag_dof("pongaterian"))
        self.assertFalse(hf._get_flag_dof("foogetarian"))

    def test_raises_exception_if_flag_has_no_dof(self):
        hf = fx.HasFlagsTestable(flag_dofs=self.flag_dofs)
        with self.assertRaises(model.flags.exceptions.FlagHasNoDOFError):
            _ = hf._get_flag_dof("alcohol_free")

    def test_raises_exception_if_dof_not_listed(self):
        hf = fx.HasFlagsTestable(flag_dofs={
            "nut_free": True,
            "vegetarian": False,
        })
        with self.assertRaises(model.flags.exceptions.UndefinedFlagError):
            _ = hf._get_flag_dof("vegan")

    def test_raises_exception_if_dof_undefined(self):
        hf = fx.HasFlagsTestable(flag_dofs=self.flag_dofs)
        with self.assertRaises(model.flags.exceptions.UndefinedFlagError):
            _ = hf._get_flag_dof("vegan")


class TestGatherAllRelatedNutrientRatios(TestCase):
    def setUp(self):
        self.nutrient_ratios = {
            "foo": mock.Mock(),
            "foobing": mock.Mock(),
            "foobar": mock.Mock(),
            "bar": mock.Mock(),
            "ping": mock.Mock()
        }

    @mock.patch.dict(model.flags.ALL_FLAGS, tests.model.flags.ALL_TEST_FLAGS)
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

    def test_empty_list_returned_if_no_related_nutrient_ratios(self):
        hf = fx.HasFlagsTestable()
        self.assertEqual(hf.gather_all_related_nutrient_ratios("pongaterian"), [])

# class TestGetFlagValue(TestCase):
