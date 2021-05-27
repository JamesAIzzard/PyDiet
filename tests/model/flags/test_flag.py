"""Tests for the flag class."""
from unittest import TestCase, mock

import model
from tests.model.nutrients import fixtures as nfx


class TestConstructor(TestCase):
    def test_makes_correct_instance(self):
        fg = model.flags.Flag("alcohol_free")
        self.assertTrue(isinstance(fg, model.flags.Flag))

    def test_raises_exception_if_flag_name_invalid(self):
        with self.assertRaises(model.flags.exceptions.FlagNameError):
            _ = model.flags.Flag("madup")


class TestName(TestCase):
    def test_name_is_correct(self):
        fg = model.flags.Flag("alcohol_free")
        self.assertEqual(fg.name, "alcohol_free")


class TestDirectAlias(TestCase):
    def test_direct_alias_is_correct(self):
        af = model.flags.Flag("alcohol_free")
        self.assertTrue(af.direct_alias)
        nf = model.flags.Flag("nut_free")
        self.assertFalse(nf.direct_alias)


class TestRelatedNutrientNames(TestCase):
    def test_related_nutrient_names_are_correct(self):
        af = model.flags.Flag("alcohol_free")
        self.assertEqual(af.related_nutrient_names, ["alcohol"])
        self.assertTrue(len(af.related_nutrient_names) == 1)


class TestGetImplicationForNutrient(TestCase):
    def test_implication_is_correct(self):
        gf = model.flags.Flag("gluten_free")
        self.assertEqual(gf.get_implication_for_nutrient("gluten"), model.flags.FlagImpliesNutrient.zero)

    def test_raises_exception_if_nutrient_unrelated(self):
        af = model.flags.Flag("alcohol_free")
        with self.assertRaises(model.flags.exceptions.NutrientNotRelatedError):
            af.get_implication_for_nutrient("protein")


class TestNutrientRatioMatchesRelation(TestCase):
    """Tests the nutrient_ratio_matches_relation method."""
    def test_returns_true_when_nutrient_matches(self):
        """Check the method returns True if the nutrient ratio matches the relation."""
        # Create a test nutrient ratio which matches a flag;
        nr = model.nutrients.NutrientRatio(
            subject=mock.Mock(),
            nutrient_name="alcohol",
            nutrient_ratio_data_src=nfx.get_nutrient_ratio_data_src(nfx.get_nutrient_ratio_data(
                nutrient_mass_g=0,
                subject_qty_g=100
            ))
        )

        # Grab the flag you want to test against;
        af = model.flags.Flag("alcohol_free")

        # Assert the flag confirms the nutrient matches;
        self.assertTrue(af.nutrient_ratio_matches_relation(nr))

    def test_returns_false_when_nutrient_does_not_match(self):
        """Check the method returns False if the nutrient ratio opposes the relation."""
        # Create a test nutrient ratio which opposes a flag;
        nr = model.nutrients.NutrientRatio(
            subject=mock.Mock(),
            nutrient_name="alcohol",
            nutrient_ratio_data_src=nfx.get_nutrient_ratio_data_src(nfx.get_nutrient_ratio_data(
                nutrient_mass_g=10,
                subject_qty_g=100
            ))
        )

        # Grab the flag you want to test against;
        af = model.flags.Flag("alcohol_free")

        # Assert the flag confirms the nutrient matches;
        self.assertFalse(af.nutrient_ratio_matches_relation(nr))
