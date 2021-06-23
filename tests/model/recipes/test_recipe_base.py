"""Tests the RecipeBase class."""
from unittest import TestCase

from tests.model.recipes import fixtures as rfx
from tests.persistence import fixtures as pfx


class TestUniqueValue(TestCase):
    """Tests the unique_value property."""

    def test_name_is_returned(self):
        """Checks that we get the recipe name back from the unique value field."""
        # Create a test instance;
        rb = rfx.RecipeBaseTestable(recipe_data=rfx.get_recipe_data(for_unique_name="Porridge"))

        # Check the property returns the name;
        self.assertEqual("Porridge", rb.unique_value)


class TestTypicalServingSizeG(TestCase):
    """Tests the typical_serving_size_property."""

    @pfx.use_test_database
    def test_correct_value_is_returned(self):
        """Checks the property returns the correct data."""
        # Create a test instance;
        rb = rfx.RecipeBaseTestable(recipe_data=rfx.get_recipe_data(for_unique_name="Banana Milkshake"))

        # Check we get the correct value;
        self.assertEqual(662.396, rb.typical_serving_size_g)


class TestNutrientRatiosData(TestCase):
    """Tests the nutrient_ratios property."""

    @pfx.use_test_database
    def test_correct_ratio_data_is_returned(self):
        """Checks the correct ratios are returned."""
        # Create a test instance of a known recipe;
        rb = rfx.RecipeBaseTestable(recipe_data=rfx.get_recipe_data(for_unique_name="Banana Milkshake"))

        # Test some of the ratios we get back;
        # Cache the ratios;
        nrs = rb.nutrient_ratios
        self.assertAlmostEqual(0.027607024887141313, nrs['protein'].subject_g_per_host_g, delta=0.0001)
        self.assertAlmostEqual(0.11695791813787698, nrs['carbohydrate'].subject_g_per_host_g, delta=0.0001)


class TestIngredientQuantities(TestCase):
    """Tests the IngredientQuantities method."""

    @pfx.use_test_database
    def test_correct_quanties_are_returned(self):
        # Create a test instance of a known recipe;
        rb = rfx.RecipeBaseTestable(recipe_data=rfx.get_recipe_data(for_unique_name="Banana Milkshake"))

        # Cache the ingredient quantities;
        iq = rb.ingredient_quantities

        # Assert the quantities are correct;
        self.assertEqual(25, iq["1198a703-ae23-4303-9b21-dd8ef9d16548"].quantity_in_g)
        self.assertEqual(487.396, iq["7b5fd211-f8ec-42c0-9853-9cb2e65ec47e"].quantity_in_g)
        self.assertEqual(150, iq["ef48e0c5-c5f0-45ac-9e3e-dcca5162a548"].quantity_in_g)


class TestIngredientRatios(TestCase):
    """Tests the IngredientQuantities method."""

    @pfx.use_test_database
    def test_correct_quanties_are_returned(self):
        # Create a test instance of a known recipe;
        rb = rfx.RecipeBaseTestable(recipe_data=rfx.get_recipe_data(for_unique_name="Banana Milkshake"))

        # Cache the ingredient ratios;
        ir = rb.ingredient_ratios

        # Assert the quantities are correct;
        self.assertEqual(25/662.396, ir["1198a703-ae23-4303-9b21-dd8ef9d16548"].subject_g_per_host_g)
        self.assertEqual(487.396/662.396, ir["7b5fd211-f8ec-42c0-9853-9cb2e65ec47e"].subject_g_per_host_g)
        self.assertEqual(150/662.396, ir["ef48e0c5-c5f0-45ac-9e3e-dcca5162a548"].subject_g_per_host_g)


class TestGetPathIntoDB(TestCase):
    """Checks the get_path_into_db property"""

    def test_correct_value_is_returned(self):
        """Check we get the correct value back from the method."""
        # Create a test instance;
        rb = rfx.RecipeBaseTestable(rfx.get_recipe_data())

        # Assert we get the right path back;
        self.assertEqual("C:/Users/james.izzard/Dropbox/pydiet/database/recipes", rb.get_path_into_db())


class TestPersistableData(TestCase):
    """Tests the persistable data property."""

    @pfx.use_test_database
    def test_correct_value_is_returned(self):
        """Checks the persistable data method returns the correct data."""
        # Grab some test data;
        data = rfx.get_recipe_data(for_unique_name="Porridge")

        # Create a test instance, passing in the data;
        rb = rfx.RecipeBaseTestable(recipe_data=data)

        # Assert we get the same data back from the persistable data property;
        self.assertEqual(
            data,
            rb.persistable_data
        )
