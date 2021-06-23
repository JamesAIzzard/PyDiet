"""Tests for the HasReadableIngredientRatios class."""
from unittest import TestCase

import model
from tests.model.ingredients import fixtures as ifx
from tests.model.quantity import fixtures as qfx
from tests.persistence import fixtures as pfx


class TestFlagDOFS(TestCase):
    """Tests the flag_dofs property."""

    def test_correct_values_are_returned(self):
        # Create a test instance, passing in known data;
        hrir = ifx.HasReadableIngredientRatiosTestable(ingredient_ratios_data={
            model.ingredients.get_df_name_from_ingredient_name("Cucumber"):
                qfx.get_qty_ratio_data(subject_qty_g=60, host_qty_g=100),
            model.ingredients.get_df_name_from_ingredient_name("Honey"):
                qfx.get_qty_ratio_data(subject_qty_g=40, host_qty_g=100)
        })

        self.assertEqual(
            {
                "nut_free": True,
                "vegan": False,
                "vegetarian": True
            },
            hrir.flag_dofs
        )


class TestCostPerG(TestCase):
    """Tests the cost_per_g property."""

    def test_correct_value_is_returned(self):
        """Checks we get the correct value back."""
        # Create a test instance, passing in known data;
        hrir = ifx.HasReadableIngredientRatiosTestable(ingredient_ratios_data={
            model.ingredients.get_df_name_from_ingredient_name("Cucumber"):
                qfx.get_qty_ratio_data(subject_qty_g=60, host_qty_g=100),
            model.ingredients.get_df_name_from_ingredient_name("Honey"):
                qfx.get_qty_ratio_data(subject_qty_g=40, host_qty_g=100)
        })

        # Assert the cost_per_g is correct;
        self.assertEqual((0.002666666666666667 * 0.6) + (0.0049 * 0.4), hrir.cost_per_g)


class TestIngredientRatios(TestCase):
    """Tests for the ingredient_ratios property"""

    @pfx.use_test_database
    def test_returns_correct_readonly_ingredient_ratios(self):
        """Check that we get the correct type and instances of ingredient ratios."""
        # Create a test instance, passing in known data;
        hrir = ifx.HasReadableIngredientRatiosTestable(ingredient_ratios_data={
            model.ingredients.get_df_name_from_ingredient_name("Cucumber"):
                qfx.get_qty_ratio_data(subject_qty_g=60, host_qty_g=100),
            model.ingredients.get_df_name_from_ingredient_name("Honey"):
                qfx.get_qty_ratio_data(subject_qty_g=40, host_qty_g=100)
        })

        # Grab the ingredient ratios;
        irs = hrir.ingredient_ratios

        # Check that we get the right number of ratios returned;
        self.assertEqual(2, len(irs))

        # Check that the ratios returned are the right type;
        for i_ratio in irs.values():
            self.assertTrue(isinstance(i_ratio, model.ingredients.ReadonlyIngredientRatio))

        # Check some of the values;
        self.assertEqual(0.6, irs[model.ingredients.get_df_name_from_ingredient_name("Cucumber")].subject_g_per_host_g)
        self.assertEqual(0.4, irs[model.ingredients.get_df_name_from_ingredient_name("Honey")].subject_g_per_host_g)

    @pfx.use_test_database
    def test_exception_if_ratios_total_greater_than_one(self):
        """Checks that we get an exception if the sum of all the ingredient ratios exceeds one."""
        # Create a test instance, passing in data with the ingredient ratios deliberately summing to greater than one;
        hrir = ifx.HasReadableIngredientRatiosTestable(ingredient_ratios_data={
            model.ingredients.get_df_name_from_ingredient_name("Cucumber"):
                qfx.get_qty_ratio_data(subject_qty_g=60, host_qty_g=100),
            model.ingredients.get_df_name_from_ingredient_name("Honey"):
                qfx.get_qty_ratio_data(subject_qty_g=50, host_qty_g=100)
        })

        # Assert we get an exception when we call for ingredient ratios;
        with self.assertRaises(model.ingredients.exceptions.IngredientRatiosSumExceedsOneError):
            _ = hrir.ingredient_ratios


class TestGetIngredientRatio(TestCase):
    """Tests the get_ingredient_ratio method."""

    @pfx.use_test_database
    def test_gets_correct_ratio(self):
        """Checks the method returns the correct ratio."""
        # Create a test instance, passing in known data;
        hrir = ifx.HasReadableIngredientRatiosTestable(ingredient_ratios_data={
            model.ingredients.get_df_name_from_ingredient_name("Cucumber"):
                qfx.get_qty_ratio_data(subject_qty_g=60, host_qty_g=100),
            model.ingredients.get_df_name_from_ingredient_name("Honey"):
                qfx.get_qty_ratio_data(subject_qty_g=50, host_qty_g=100)
        })

        # Grab one of the ratios;
        cuc = hrir.get_ingredient_ratio(ingredient_unique_name="Cucumber")

        # Check that the ratio is the right type;
        self.assertTrue(isinstance(cuc, model.ingredients.ReadonlyIngredientRatio))

        # Check that the ratio has the right value;
        self.assertEqual(0.6, cuc.subject_g_per_host_g)


class TestIngredientUniqueNames(TestCase):
    """Tests the ingredient_unique_names property."""

    @pfx.use_test_database
    def test_returns_correct_names(self):
        """Checks that the property returns the correct names."""
        # Create a test instance, passing in known data;
        hrir = ifx.HasReadableIngredientRatiosTestable(ingredient_ratios_data={
            model.ingredients.get_df_name_from_ingredient_name("Cucumber"):
                qfx.get_qty_ratio_data(subject_qty_g=60, host_qty_g=100),
            model.ingredients.get_df_name_from_ingredient_name("Honey"):
                qfx.get_qty_ratio_data(subject_qty_g=50, host_qty_g=100)
        })

        self.assertEqual({"Cucumber", "Honey"}, set(hrir.ingredient_unique_names))


class TestNutrientRatiosData(TestCase):
    """Tests for the nutrient_ratios_data property."""

    @pfx.use_test_database
    def test_data_matches_single_ingredient_if_only_one_ingredient_provided(self):
        """Checks the data matches a single ingredient when only one is provided."""
        # Create a test instance with a single ingredient.
        hrir = ifx.HasReadableIngredientRatiosTestable(ingredient_ratios_data={
            model.ingredients.get_df_name_from_ingredient_name("Tuna"):
                qfx.get_qty_ratio_data(subject_qty_g=100, host_qty_g=100),
        })

        self.assertEqual(0.308, hrir.get_nutrient_ratio("protein").subject_g_per_host_g)
        self.assertEqual(0.005, hrir.get_nutrient_ratio("carbohydrate").subject_g_per_host_g)

    @pfx.use_test_database
    def test_correct_data_is_returned(self):
        """Checks we get the correct data back."""
        # Create a test instance, passing in some known ingredient ratios;
        hrir = ifx.HasReadableIngredientRatiosTestable(ingredient_ratios_data={
            model.ingredients.get_df_name_from_ingredient_name("Cucumber"):
                qfx.get_qty_ratio_data(subject_qty_g=100, host_qty_g=125),
            model.ingredients.get_df_name_from_ingredient_name("Honey"):
                qfx.get_qty_ratio_data(subject_qty_g=5, host_qty_g=125),
            model.ingredients.get_df_name_from_ingredient_name("Tuna"):
                qfx.get_qty_ratio_data(subject_qty_g=20, host_qty_g=125)
        })

        # Check some of the ratios;
        self.assertAlmostEqual(0.05481333333333334, hrir.get_nutrient_ratio("protein").subject_g_per_host_g)
        self.assertAlmostEqual(0.06042666666666668, hrir.get_nutrient_ratio("carbohydrate").subject_g_per_host_g)
