"""Tests for the ReadonlyRecipe class."""
from unittest import TestCase

import model
import persistence
from tests.model.ingredients import fixtures as ifx
from tests.model.recipes import fixtures as rfx
from tests.persistence import fixtures as pfx


class TestConstructor(TestCase):
    """Tests the constructor function."""

    @pfx.use_test_database
    def test_can_construct_simple_instance(self):
        """Checks we can construct a simple instance."""
        self.assertTrue(isinstance(
            model.recipes.ReadonlyRecipe(recipe_data_src=lambda: rfx.get_recipe_data(
                for_unique_name="Porridge"
            )),
            model.recipes.ReadonlyRecipe
        ))

    @pfx.use_test_database
    def test_data_is_loaded_correctly(self):
        """Checks any data that is passed in gets loaded correctly."""
        # Grab some test data;
        rd = rfx.get_recipe_data(for_unique_name="Porridge")

        # Create a test instance, passing in some data;
        rr = model.recipes.ReadonlyRecipe(recipe_data_src=lambda: rd)

        # Assert that the persistable data is the same data that we passed in;
        self.assertEqual(rd, rr.persistable_data)

    @pfx.use_test_database
    def test_datafile_name_is_populated(self):
        """Checks that the datafile name is populated, if we pass data in."""
        # Grab the datafile name for a known recipe;
        df_name = persistence.get_datafile_name_for_unique_value(
            cls=model.recipes.RecipeBase,
            unique_value="Porridge"
        )

        # Create a test instance for this recipe;
        sr = model.recipes.ReadonlyRecipe(recipe_data_src=model.recipes.get_recipe_data_src(
            for_unique_name="Porridge"
        ))

        # Assert that the datafile name has been populated;
        self.assertEqual(df_name, sr.datafile_name)


class TestName(TestCase):
    """Tests for the name property."""

    def test_name_is_correct(self):
        """Checks that the name property is returned correctly."""
        # Create a test instance with known name;
        sr = model.recipes.ReadonlyRecipe(recipe_data_src=model.recipes.get_recipe_data_src(
            for_unique_name="Porridge"
        ))

        # Assert that the name returns the correct value;
        self.assertEqual("Porridge", sr.name)


class TestIngredientQuantitiesData(TestCase):
    """Tests for the ingredient_quantities_data property."""

    @pfx.use_test_database
    def test_correct_data_is_returned(self):
        """Checks the ingredient quantities data is returned correctly."""
        # Grab the ingredient quantities data from a known recipe;
        iqd = rfx.get_recipe_data(for_unique_name="Porridge")['ingredient_quantities_data']

        # Create a test instance;
        sr = model.recipes.ReadonlyRecipe(recipe_data_src=model.recipes.get_recipe_data_src(
            for_unique_name="Porridge"
        ))

        # Assert the recipe instance's ingredient quantities data is the same as it should be;
        self.assertEqual(iqd, sr.ingredient_quantities_data)


class TestIngredientQuantities(TestCase):
    """Tests for the ingredient_quantities method, in the context of ReadonlyRecipe."""

    @pfx.use_test_database
    def test_correct_ingredient_quantities_are_returned(self):
        """Checks that a recipe instance returns the correct ingredient quantities."""
        # Create a test instance;
        sr = model.recipes.ReadonlyRecipe(recipe_data_src=model.recipes.get_recipe_data_src(
            for_unique_name="Porridge"
        ))

        # Assert we get three ingredient quantities;
        self.assertEqual(3, len(sr.ingredient_quantities))

        # Assert they are the correct Readonly type;
        for iq in sr.ingredient_quantities.values():
            self.assertTrue(iq, model.ingredients.ReadonlyIngredientQuantity)

        # Check that we have the correct quantities of each ingredient;
        self.assertEqual(
            60,
            sr.ingredient_quantities[ifx.get_ingredient_df_name("Oats (Whole)")].quantity_in_g
        )
        self.assertEqual(
            15,
            sr.ingredient_quantities[ifx.get_ingredient_df_name("Sultana")].quantity_in_g
        )
        self.assertEqual(
            100,
            sr.ingredient_quantities[ifx.get_ingredient_df_name("Milk (Skimmed)")].ref_qty
        )


class TestServeIntervalsData(TestCase):
    """Tests for the serve_intervals property."""

    @pfx.use_test_database
    def test_single_serve_interval_is_returned_correctly(self):
        """Checks the method returns the correct serve intervals."""
        # Create a test instance;
        sr = model.recipes.ReadonlyRecipe(recipe_data_src=model.recipes.get_recipe_data_src(
            for_unique_name="Porridge"
        ))

        # Assert the correct intervals are returned;
        self.assertEqual(
            ["04:00-10:00"],
            sr.serve_intervals_data
        )

    @pfx.use_test_database
    def test_multiple_serve_intervals_returned_correctly(self):
        """Checks the method returns the correct serve intervals."""
        # Create a test instance;
        sr = model.recipes.ReadonlyRecipe(recipe_data_src=model.recipes.get_recipe_data_src(
            for_unique_name="Banana Milkshake"
        ))

        # Assert the correct intervals are returned;
        self.assertEqual(
            {"04:00-10:00", "12:00-13:00", "16:00-18:00"},
            set(sr.serve_intervals_data)
        )


class TestInstructionSrc(TestCase):
    """Tests the instruction_src property."""

    @pfx.use_test_database
    def test_correct_src_is_returned(self):
        """Check the correct source is returned."""
        # Create a test instance;
        sr = model.recipes.ReadonlyRecipe(recipe_data_src=model.recipes.get_recipe_data_src(
            for_unique_name="Banana Milkshake"
        ))

        # Assert the correct data source is required;
        self.assertEqual(
            "https://www.bbcgoodfood.com/recipes/banana-milkshake",
            sr.instruction_src
        )


class TestTags(TestCase):
    """Tests the tags property."""

    @pfx.use_test_database
    def test_correct_tags_are_returned(self):
        """Checks that the correct tags are returned."""
        # Create a test instance;
        sr = model.recipes.ReadonlyRecipe(recipe_data_src=model.recipes.get_recipe_data_src(
            for_unique_name="Banana Milkshake"
        ))

        # Assert the correct tags are returned;
        self.assertEqual(
            {"drink", "sweet"},
            set(sr.tags)
        )
