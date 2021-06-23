"""Tests for the HasReadableRecipeQuantities class."""
from unittest import TestCase

import model
from tests.model.recipes import fixtures as rfx
from tests.persistence import fixtures as pfx


class TestRecipeRatiosData(TestCase):
    """Tests for the recipe_ratios_data property."""

    @pfx.use_test_database
    def test_correct_data_is_returned(self):
        """Checks the method returns the correct data."""
        # Create a test instance, passing some known data in;
        hrrq = rfx.HasReadableRecipeQuantitiesTestable(recipe_quantities_data={
            model.recipes.get_datafile_name_for_unique_value("Banana Milkshake"): model.quantity.QuantityData(
                quantity_in_g=100,
                pref_unit='g'
            ),
            model.recipes.get_datafile_name_for_unique_value("Peanut Butter Toast"): model.quantity.QuantityData(
                quantity_in_g=200,
                pref_unit='g'
            )
        })

        # Cache the recipe ratios dict;
        rr = hrrq.recipe_ratios_data

        # Check we get the correct number of entries in the recipe ratios dict;
        self.assertEqual(2, len(rr))

        # Check the ratio values are correct;
        self.assertEqual(
            1 / 3, model.quantity.get_ratio_from_qty_ratio_data(
                rr[model.recipes.get_datafile_name_for_unique_value("Banana Milkshake")]
            )
        )
        self.assertEqual(
            2 / 3, model.quantity.get_ratio_from_qty_ratio_data(
                rr[model.recipes.get_datafile_name_for_unique_value("Peanut Butter Toast")]
            )
        )


class TestIngredientQuantitiesData(TestCase):
    """Tests for the ingredient_quantities_data property."""

    @pfx.use_test_database
    def test_correct_quantities_returned(self):
        """Checks we get the right ingredient quantities data back."""
        # Create a test instance, passing some known data in;
        hrrq = rfx.HasReadableRecipeQuantitiesTestable(recipe_quantities_data={
            model.recipes.get_datafile_name_for_unique_value("Bread and Butter"): model.quantity.QuantityData(
                quantity_in_g=100,
                pref_unit='g'
            ),
            model.recipes.get_datafile_name_for_unique_value("Peanut Butter Toast"): model.quantity.QuantityData(
                quantity_in_g=200,
                pref_unit='g'
            )
        })

        # Collect the ingredient quantities data;
        iqd = hrrq.ingredient_quantities_data

        # Assert there are the right number of entries;
        self.assertEqual(3, len(iqd))

        # Assert the quantities are correct;
        self.assertEqual(
            0.7703081232492996 * 300,
            iqd[model.ingredients.get_df_name_from_ingredient_name("Bread (Wholemeal)")]["quantity_in_g"]
        )
        self.assertEqual(
            0.10270774976657329 * 300,
            iqd[model.ingredients.get_df_name_from_ingredient_name("Butter")]["quantity_in_g"]
        )
        self.assertEqual(
            0.12698412698412698 * 300,
            iqd[model.ingredients.get_df_name_from_ingredient_name("Peanut Butter")]["quantity_in_g"]
        )


class TestRecipeQuantities(TestCase):
    """Tests for the recipe quantities property."""

    @pfx.use_test_database
    def test_correct_values_returned(self):
        """Checks we get the right values back."""
        # Create a test instance, passing some known data in;
        hrrq = rfx.HasReadableRecipeQuantitiesTestable(recipe_quantities_data={
            model.recipes.get_datafile_name_for_unique_value("Bread and Butter"): model.quantity.QuantityData(
                quantity_in_g=100,
                pref_unit='g'
            ),
            model.recipes.get_datafile_name_for_unique_value("Peanut Butter Toast"): model.quantity.QuantityData(
                quantity_in_g=200,
                pref_unit='g'
            )
        })

        # Grab the recipe quantities;
        rqs = hrrq.recipe_quantities

        # Check we get the right number of items back;
        self.assertEqual(2, len(rqs))
        # Check the instances are the right type;
        for rq in rqs.values():
            self.assertTrue(isinstance(rq, model.recipes.ReadonlyRecipeQuantity))
        # Check the quantites are correct;
        self.assertEqual(100, rqs[model.recipes.get_datafile_name_for_unique_value("Bread and Butter")].quantity_in_g)
        self.assertEqual(200,
                         rqs[model.recipes.get_datafile_name_for_unique_value("Peanut Butter Toast")].quantity_in_g)


class TotalRecipesMassG(TestCase):
    """Tests for the total_recipes_mass_g property."""

    @pfx.use_test_database
    def test_value_is_correct(self):
        """Checks the property returns the correct mass."""
        # Create a test instance, passing some known data in;
        hrrq = rfx.HasReadableRecipeQuantitiesTestable(recipe_quantities_data={
            model.recipes.get_datafile_name_for_unique_value("Bread and Butter"): model.quantity.QuantityData(
                quantity_in_g=100,
                pref_unit='g'
            ),
            model.recipes.get_datafile_name_for_unique_value("Peanut Butter Toast"): model.quantity.QuantityData(
                quantity_in_g=200,
                pref_unit='g'
            )
        })

        # Check the mass is correct;
        self.assertEqual(300, hrrq.total_recipes_mass_g)
