"""Tests for the IngredientBase class."""
from unittest import TestCase

import model
import persistence
from tests.model.ingredients import fixtures as fx
from tests.persistence import fixtures as pfx


class TestGetPathIntoDB(TestCase):
    """Tests get_path_into_db property."""

    @pfx.use_test_database
    def test_correct_path_is_returned(self):
        """Checks the correct path is returned."""
        # Create a test instance;
        ib = fx.IngredientBaseTestable(fx.get_ingredient_data())

        # Assert correct path is returned;
        self.assertEqual(
            f"{persistence.configs.path_into_db}/ingredients",
            ib.get_path_into_db()
        )


class TestMissingMandatoryAttrs(TestCase):
    """Tests the missing_mandatory_attrs property on the Ingredient class."""

    @pfx.use_test_database
    def test_list_empty_if_ingredient_completely_defined(self):
        """Checks we don't get any missing attributes if the data is fully defined;"""
        # Create a test instance with fully defined data;
        i = fx.IngredientBaseTestable(ingredient_data=fx.get_ingredient_data(
            for_unique_name=fx.get_ingredient_name_with(characteristic="typical_fully_defined_data")
        ))

        # Assert that the list is empty;
        self.assertEqual(0, len(i.missing_mandatory_attrs))

    @pfx.use_test_database
    def test_cost_listed_if_cost_undefined(self):
        """Checks we don't get any missing attributes if the data is fully defined;"""
        # Create a test instance with an undefined cost;
        i = fx.IngredientBaseTestable(ingredient_data=fx.get_ingredient_data(
            for_unique_name=fx.get_ingredient_name_with(characteristic="cost_per_g_undefined")
        ))

        # Assert that the list is empty;
        self.assertEqual({"cost"}, set(i.missing_mandatory_attrs))

    @pfx.use_test_database
    def test_mandatory_nutrient_ratios_listed_when_undefined(self):
        """Checks we get the mandatory attributes listed if any are undefined."""
        # Create an instance with some mandatory nutrient ratios missing;
        i = fx.IngredientBaseTestable(ingredient_data=fx.get_ingredient_data(
            for_unique_name=fx.get_ingredient_name_with(characteristic="nutrient_ratios_protein_carbs_undefined")
        ))

        # Assert that the missing nutrients show up in the missing attrs list;
        self.assertTrue("protein" in i.missing_mandatory_attrs)
        self.assertTrue("carbohydrate" in i.missing_mandatory_attrs)
