"""Tests for the flag class."""
from unittest import TestCase, mock

import model
from tests.model.quantity import fixtures as qfx


class TestConstructor(TestCase):
    """Tests the constructor."""
    def test_can_make_instance(self):
        """Check we can create an instance."""
        # Create an instance;
        fg = model.flags.Flag("alcohol_free")

        # Check it is the right type;
        self.assertTrue(isinstance(fg, model.flags.Flag))

    def test_raises_exception_if_flag_name_invalid(self):
        # Check we get an exception if we try to create a flag with a name not in the config;
        with self.assertRaises(model.flags.exceptions.FlagNameError):
            _ = model.flags.Flag("madup")


class TestName(TestCase):
    """Tests the name property."""
    def test_name_is_correct(self):
        """Check we get the correct name out of the name property."""
        # Create a test instance with a specific name;
        fg = model.flags.Flag("alcohol_free")
        # Check the name property gives us the same name back;
        self.assertEqual(fg.name, "alcohol_free")


class TestDirectAlias(TestCase):
    """Tests the direct alias property."""
    def test_direct_alias_is_correct(self):
        """Check we get the correct result out of the direct alias property."""
        # Create a flag we know is a direct alias;
        af = model.flags.Flag("alcohol_free")
        # Assert the property returns True;
        self.assertTrue(af.direct_alias)

        # Create a flag we know is not a direct alias;
        nf = model.flags.Flag("nut_free")
        # Assert the property returns False;
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
        nr = model.nutrients.ReadonlyNutrientRatio(
            nutrient_name="alcohol",
            ratio_host=mock.Mock(),
            qty_ratio_data_src=qfx.get_qty_ratio_data_src(qfx.get_qty_ratio_data(
                subject_qty_g=0,
                host_qty_g=100
            ))
        )

        # Grab the flag you want to test against;
        af = model.flags.Flag("alcohol_free")

        # Assert the flag confirms the nutrient matches;
        self.assertTrue(af.nutrient_ratio_matches_relation(nr))

    def test_returns_false_when_nutrient_does_not_match(self):
        """Check the method returns False if the nutrient ratio opposes the relation."""
        # Create a test nutrient ratio which opposes a flag;
        nr = model.nutrients.ReadonlyNutrientRatio(
            ratio_host=mock.Mock(),
            nutrient_name="alcohol",
            qty_ratio_data_src=qfx.get_qty_ratio_data_src(qfx.get_qty_ratio_data(
                subject_qty_g=10,
                host_qty_g=100
            ))
        )

        # Grab the flag you want to test against;
        af = model.flags.Flag("alcohol_free")

        # Assert the flag confirms the nutrient matches;
        self.assertFalse(af.nutrient_ratio_matches_relation(nr))
