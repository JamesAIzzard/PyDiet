from unittest import TestCase

import model
from tests.model.flags import fixtures as fx


class TestConstructor(TestCase):
    def test_makes_correct_instance(self):
        hf = fx.HasFlagsTestable()
        self.assertTrue(isinstance(hf, model.flags.HasFlags))


class TestGetFlagDOF(TestCase):
    def test_gets_dof_correctly(self):
        hf = fx.HasFlagsTestable({"nut_free": True})
        self.assertTrue(hf.get_flag_dof("nut_free"))
        hf = fx.HasFlagsTestable({"nut_free": False})
        self.assertFalse(hf.get_flag_dof("nut_free"))

    def test_raises_exception_if_flag_has_no_dof(self):
        hf = fx.HasFlagsTestable({"alcohol_free": True})
        with self.assertRaises(model.flags.exceptions.FlagHasNoDOFError):
            _ = hf.get_flag_dof("alcohol_free")

    def test_raises_exception_if_dof_not_listed(self):
        hf = fx.HasFlagsTestable({"alcohol_free": True})
        with self.assertRaises(model.flags.exceptions.UndefinedFlagError):
            _ = hf.get_flag_dof("nut_free")

    def test_raises_exception_if_dof_undefined(self):
        hf = fx.HasFlagsTestable({"nut_free": None})
        with self.assertRaises(model.flags.exceptions.UndefinedFlagError):
            _ = hf.get_flag_dof("nut_free")


class GatherAllRelatedNutrientRatios(TestCase):
    def test_correct_nutrient_ratios_returned(self):
        hf = fx.HasFlagsTestable()
        self.assertEqual(
            hf.gather_all_related_nutrient_ratios("alcohol_free"),
            model.nutrients.GLOBAL_NUTRIENTS["alcohol"]
        )
