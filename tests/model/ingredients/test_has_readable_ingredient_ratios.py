"""Tests for the HasReadableIngredientRatios class."""
from unittest import TestCase
from typing import List

import model
from tests.model.ingredients import fixtures as ifx
from tests.model.quantity import fixtures as qfx


class TestIngredientRatios(TestCase):
    """Tests for the ingredient_ratios property"""

    def test_returns_correct_readonly_ingredient_ratios(self):
        """Check that we get the correct type and instances of ingredient ratios."""
        # Create a test instance, passing in known data;
        hrir = ifx.HasReadableIngredientRatiosTestable(ingredient_ratios_data={
            model.ingredients.get_df_name_from_ingredient_name("Cucumber"):
                qfx.get_qty_ratio_data(subject_qty_g=60, host_qty_g=100),
            model.ingredients.get_df_name_from_ingredient_name("Honey"):
                qfx.get_qty_ratio_data(subject_qty_g=50, host_qty_g=100)
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
        self.assertEqual(0.5, irs[model.ingredients.get_df_name_from_ingredient_name("Honey")].subject_g_per_host_g)


class TestGetIngredientRatio(TestCase):
    """Tests the get_ingredient_ratio method."""
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
