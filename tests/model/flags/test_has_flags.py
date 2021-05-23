"""Tests for HasFlags functionality."""
from unittest import TestCase

import model
import tests.model.nutrients.fixtures as nfx
from tests.model.flags import fixtures as fx


class TestConstructor(TestCase):
    def test_makes_correct_instance(self):
        hf = fx.HasFlagsTestable()
        self.assertTrue(isinstance(hf, model.flags.HasFlags))


class TestGetFlagDOF(TestCase):
    def setUp(self) -> None:
        """Setup"""
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


class TestGetFlagValue(TestCase):
    """Tests the get_flag_value method."""
    @fx.use_test_flags
    @nfx.use_test_nutrients
    def test_direct_alias_returns_true_when_all_related_nutrients_agree(self):
        """Check that a direct alias flag returns True if all related nutrients agree."""
        nutrient_ratios_data = {
            "foo": nfx.get_nutrient_ratio_data(nutrient_mass_g=0, subject_qty_g=100),
            "foobing": nfx.get_nutrient_ratio_data(nutrient_mass_g=0.9, subject_qty_g=100),
            "foobar": nfx.get_nutrient_ratio_data(nutrient_mass_g=0, subject_qty_g=100)
        }
        hf = fx.HasFlagsTestable(nutrient_ratios_data=nutrient_ratios_data)
        self.assertTrue(hf.get_flag_value("foo_free"))

    @fx.use_test_flags
    @nfx.use_test_nutrients
    def test_direct_alias_returns_false_if_nutrient_conflicts_even_with_undefined_nutrients(self):
        nutrient_ratios_data = {
            "foo": nfx.get_nutrient_ratio_data(nutrient_mass_g=0, subject_qty_g=100),
            "foobing": nfx.get_nutrient_ratio_data(nutrient_mass_g=0, subject_qty_g=100),
        }
        hf = fx.HasFlagsTestable(nutrient_ratios_data=nutrient_ratios_data)
        self.assertFalse(hf.get_flag_value("foo_free"))

    @fx.use_test_flags
    @nfx.use_test_nutrients
    def test_direct_alias_returns_false_when_a_related_nutrient_disagrees(self):
        nutrient_ratios_data = {
            "foo": nfx.get_nutrient_ratio_data(nutrient_mass_g=0, subject_qty_g=100),
            "foobing": nfx.get_nutrient_ratio_data(nutrient_mass_g=0, subject_qty_g=100),
            "foobar": nfx.get_nutrient_ratio_data(nutrient_mass_g=0, subject_qty_g=100)
        }
        hf = fx.HasFlagsTestable(nutrient_ratios_data=nutrient_ratios_data)
        self.assertFalse(hf.get_flag_value("foo_free"))

    @fx.use_test_flags
    @nfx.use_test_nutrients
    def test_direct_alias_raises_exception_when_related_nutrient_undefined(self):
        nutrient_ratios_data = {
            "foo": nfx.get_nutrient_ratio_data(nutrient_mass_g=0, subject_qty_g=100),
            "foobar": nfx.get_nutrient_ratio_data(nutrient_mass_g=0, subject_qty_g=100)
        }
        hf = fx.HasFlagsTestable(nutrient_ratios_data=nutrient_ratios_data)
        with self.assertRaises(model.flags.exceptions.UndefinedFlagError):
            hf.get_flag_value("foo_free")

    @fx.use_test_flags
    def test_returns_dof_when_flag_has_no_related_nutrients(self):
        hf = fx.HasFlagsTestable(flag_dofs={"foogetarian": True})
        self.assertTrue(hf.get_flag_value("foogetarian"))
        hf = fx.HasFlagsTestable(flag_dofs={"foogetarian": False})
        self.assertFalse(hf.get_flag_value("foogetarian"))

    @fx.use_test_flags
    @nfx.use_test_nutrients
    def test_returns_dof_if_related_nutrient_is_undefined_but_no_related_nutrients_conflict(self):
        nutrient_ratios_data = {
            "foo": nfx.get_nutrient_ratio_data(nutrient_mass_g=0, subject_qty_g=100),
            "foobing": nfx.get_nutrient_ratio_data(nutrient_mass_g=0, subject_qty_g=100),
        }
        hf = fx.HasFlagsTestable(flag_dofs={"pongaterian": True}, nutrient_ratios_data=nutrient_ratios_data)
        self.assertTrue(hf.get_flag_value("pongaterian"))
        hf = fx.HasFlagsTestable(flag_dofs={"pongaterian": False}, nutrient_ratios_data=nutrient_ratios_data)
        self.assertFalse(hf.get_flag_value("pongaterian"))

    @fx.use_test_flags
    @nfx.use_test_nutrients
    def test_dof_overrides_related_nutrients_when_no_conflict(self):
        nutrient_ratios_data = {
            "foo": nfx.get_nutrient_ratio_data(nutrient_mass_g=0, subject_qty_g=100),
            "foobing": nfx.get_nutrient_ratio_data(nutrient_mass_g=0, subject_qty_g=100),
            "bazing": nfx.get_nutrient_ratio_data(nutrient_mass_g=90, subject_qty_g=100)
        }
        hf = fx.HasFlagsTestable(flag_dofs={"pongaterian": True}, nutrient_ratios_data=nutrient_ratios_data)
        self.assertTrue(hf.get_flag_value("pongaterian"))
        hf = fx.HasFlagsTestable(flag_dofs={"pongaterian": False}, nutrient_ratios_data=nutrient_ratios_data)
        self.assertFalse(hf.get_flag_value("pongaterian"))

    @fx.use_test_flags
    def test_raises_exception_if_no_related_nutrients_and_dof_unset(self):
        hf = fx.HasFlagsTestable()
        with self.assertRaises(model.flags.exceptions.UndefinedFlagError):
            hf.get_flag_value("foogetarian")

    @fx.use_test_flags
    @nfx.use_test_nutrients
    def test_raises_exception_if_direct_alias_and_no_related_nutrients_set(self):
        hf = fx.HasFlagsTestable()
        with self.assertRaises(model.flags.exceptions.UndefinedFlagError):
            hf.get_flag_value("foo_free")

    @fx.use_test_flags
    @nfx.use_test_nutrients
    def test_returns_false_if_dof_is_true_but_nutrient_conflicts(self):
        nutrient_ratios_data = {
            "foo": nfx.get_nutrient_ratio_data(nutrient_mass_g=0, subject_qty_g=100),
            "foobing": nfx.get_nutrient_ratio_data(nutrient_mass_g=0, subject_qty_g=100),
            "bazing": nfx.get_nutrient_ratio_data(nutrient_mass_g=0, subject_qty_g=100)
        }
        hf = fx.HasFlagsTestable(flag_dofs={"pongaterian": True}, nutrient_ratios_data=nutrient_ratios_data)
        self.assertFalse(hf.get_flag_value("pongaterian"))


class TestGetUndefinedFlagNames(TestCase):
    @fx.use_test_flags
    @nfx.use_test_nutrients
    def test_returns_names_correctly(self):
        nutrient_ratios_data = {
            "foo": nfx.get_nutrient_ratio_data(nutrient_mass_g=0, subject_qty_g=100),
            "foobing": nfx.get_nutrient_ratio_data(nutrient_mass_g=90, subject_qty_g=100),
            "bazing": nfx.get_nutrient_ratio_data(nutrient_mass_g=0, subject_qty_g=100)
        }
        flag_dofs = {
            "pongaterian": True,
            "foogetarian": False
        }
        hf = fx.HasFlagsTestable(flag_dofs=flag_dofs, nutrient_ratios_data=nutrient_ratios_data)
        self.assertEqual(
            set(hf.undefined_flag_names),
            {"foo_free", "bar_free", "tirbur_free"}
        )


class TestPersistableData(TestCase):
    @fx.use_test_flags
    @nfx.use_test_nutrients
    def test_returns_correct_data(self):
        flag_dofs = {
            "bar_free": True,
            "foogetarian": False
        }
        hf = fx.HasFlagsTestable(flag_dofs=flag_dofs)
        self.assertEqual(
            hf.persistable_data['flag_data'],
            {"bar_free": True, "foogetarian": False}
        )
