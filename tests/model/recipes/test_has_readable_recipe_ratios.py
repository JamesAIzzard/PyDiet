"""Tests for the HasReadableRecipeRatios class."""
from unittest import TestCase

import model.recipes
from tests.model.recipes import fixtures as rfx
from tests.persistence import fixtures as pfx


class TestIngredientRatiosData(TestCase):
    """Tests for the ingredient_ratios_data property."""

    @pfx.use_test_database
    def test_correct_data_is_returned(self):
        """Checks that the correct ingredient ratios data is returned."""
        # Create a test instance with multiple recipes with overlapping ingredients;
        hrrr = rfx.HasReadableRecipeRatiosTestable(recipe_ratios_data={
            model.recipes.get_datafile_name_for_unique_value("Bread and Butter"): model.quantity.QuantityRatioData(
                subject_qty_data=model.quantity.QuantityData(
                    quantity_in_g=100,
                    pref_unit='g'
                ),
                host_qty_data=model.quantity.QuantityData(
                    quantity_in_g=250,
                    pref_unit='g'
                )
            ),
            model.recipes.get_datafile_name_for_unique_value("Peanut Butter Toast"): model.quantity.QuantityRatioData(
                subject_qty_data=model.quantity.QuantityData(
                    quantity_in_g=150,
                    pref_unit='g'
                ),
                host_qty_data=model.quantity.QuantityData(
                    quantity_in_g=250,
                    pref_unit='g'
                )
            ),
        })

        # Check the correct ingredients are returned;
        self.assertEqual({
            "Bread (Wholemeal)",
            "Butter",
            "Peanut Butter"
        }, set(hrrr.ingredient_unique_names))

        # Check the ratios are Readonly
        for ratio in hrrr.ingredient_ratios.values():
            self.assertTrue(isinstance(ratio, model.ingredients.ReadonlyIngredientRatio))

        # Check that the correct ingredient ratios are returned;
        self.assertAlmostEqual(0.7815126050420168, hrrr.get_ingredient_ratio("Bread (Wholemeal)").subject_g_per_host_g,
                               delta=0.00001)
        self.assertAlmostEqual(0.1042016806722689, hrrr.get_ingredient_ratio("Butter").subject_g_per_host_g,
                               delta=0.00001)
        self.assertAlmostEqual(0.11428571428571427, hrrr.get_ingredient_ratio("Peanut Butter").subject_g_per_host_g,
                               delta=0.00001)


class TestGetRecipeRatio(TestCase):
    """Tests for the get_recipe_ratio method."""

    @pfx.use_test_database
    def test_gets_correct_recipe_ratio(self):
        """Checks that the correct recipe ratio is returned."""
        # Create a test instance with some known recipes;
        hrrr = rfx.HasReadableRecipeRatiosTestable(recipe_ratios_data={
            model.recipes.get_datafile_name_for_unique_value("Bread and Butter"): model.quantity.QuantityRatioData(
                subject_qty_data=model.quantity.QuantityData(
                    quantity_in_g=100,
                    pref_unit='g'
                ),
                host_qty_data=model.quantity.QuantityData(
                    quantity_in_g=250,
                    pref_unit='g'
                )
            ),
            model.recipes.get_datafile_name_for_unique_value("Peanut Butter Toast"): model.quantity.QuantityRatioData(
                subject_qty_data=model.quantity.QuantityData(
                    quantity_in_g=150,
                    pref_unit='g'
                ),
                host_qty_data=model.quantity.QuantityData(
                    quantity_in_g=250,
                    pref_unit='g'
                )
            )
        })

        # Grab a recipe ratio back;
        rr = hrrr.get_recipe_ratio(unique_name="Bread and Butter")

        # Check it was the correct type;
        self.assertTrue(isinstance(rr, model.recipes.ReadonlyRecipeRatio))

        # Check it has the correct name;
        self.assertEqual("Bread and Butter", rr.recipe.name)

        # Check it has the correct ratio;
        self.assertAlmostEqual(100 / 250, hrrr.get_recipe_ratio("Bread and Butter").subject_g_per_host_g,
                               delta=0.00001)


class TestRecipeRatios(TestCase):
    """Tests for recipe_ratios property."""

    @pfx.use_test_database
    def test_correct_ratios_returned(self):
        """Checks that the correct ratios are returned."""
        # Create a test instance with some known recipes;
        hrrr = rfx.HasReadableRecipeRatiosTestable(recipe_ratios_data={
            model.recipes.get_datafile_name_for_unique_value("Bread and Butter"): model.quantity.QuantityRatioData(
                subject_qty_data=model.quantity.QuantityData(
                    quantity_in_g=100,
                    pref_unit='g'
                ),
                host_qty_data=model.quantity.QuantityData(
                    quantity_in_g=250,
                    pref_unit='g'
                )
            ),
            model.recipes.get_datafile_name_for_unique_value("Peanut Butter Toast"): model.quantity.QuantityRatioData(
                subject_qty_data=model.quantity.QuantityData(
                    quantity_in_g=150,
                    pref_unit='g'
                ),
                host_qty_data=model.quantity.QuantityData(
                    quantity_in_g=250,
                    pref_unit='g'
                )
            )
        })

        # Grab the ratios;
        ratios = hrrr.recipe_ratios

        # Check there are two recipes;
        self.assertEqual(2, len(ratios))

        # Check that all the ratios are the correct type;
        for ratio in ratios.values():
            self.assertTrue(isinstance(ratio, model.recipes.ReadonlyRecipeRatio))

        # Check the ratio values;
        self.assertEqual(
            100 / 250,
            ratios[model.recipes.get_datafile_name_for_unique_value("Bread and Butter")].subject_g_per_host_g
        )
        self.assertEqual(
            150 / 250,
            ratios[model.recipes.get_datafile_name_for_unique_value("Peanut Butter Toast")].subject_g_per_host_g
        )


class TestUniqueRecipeNames(TestCase):
    """Tests for the unique_recipe_names property."""

    @pfx.use_test_database
    def test_correct_names_returned(self):
        # Create a test instance with some known recipes;
        hrrr = rfx.HasReadableRecipeRatiosTestable(recipe_ratios_data={
            model.recipes.get_datafile_name_for_unique_value("Bread and Butter"): model.quantity.QuantityRatioData(
                subject_qty_data=model.quantity.QuantityData(
                    quantity_in_g=100,
                    pref_unit='g'
                ),
                host_qty_data=model.quantity.QuantityData(
                    quantity_in_g=250,
                    pref_unit='g'
                )
            ),
            model.recipes.get_datafile_name_for_unique_value("Peanut Butter Toast"): model.quantity.QuantityRatioData(
                subject_qty_data=model.quantity.QuantityData(
                    quantity_in_g=150,
                    pref_unit='g'
                ),
                host_qty_data=model.quantity.QuantityData(
                    quantity_in_g=250,
                    pref_unit='g'
                )
            )
        })

        # Assert the correct names are returned;
        self.assertEqual(
            {"Bread and Butter", "Peanut Butter Toast"},
            set(hrrr.unique_recipe_names)
        )
