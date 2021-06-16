"""Tests for the MealBase class."""
from unittest import TestCase

import model.meals
from tests.model.recipes import fixtures as rfx
from tests.model.quantity import fixtures as qfx
from tests.persistence import fixtures as pfx


class TestConstructor(TestCase):
    """Tests the constructor function."""

    def test_can_create_simple_instance(self):
        """Checks we can create a simple instance."""
        self.assertTrue(model.meals.SettableMeal(), model.meals.SettableMeal)

    @pfx.use_test_database
    def test_loads_data_if_provided(self):
        """Checks the meal instance loads any meals data that we pass in."""
        # Create some test data;
        data = {
            model.recipes.get_datafile_name_for_unique_value("Porridge"): qfx.get_qty_data(500),
            model.recipes.get_datafile_name_for_unique_value("Banana Milkshake"): qfx.get_qty_data(300),
            model.recipes.get_datafile_name_for_unique_value("Avocado and Prawns"): qfx.get_qty_data(200)
        }

        # Create a test instance, passing this data in;
        sm = model.meals.SettableMeal(meal_data=data)

        # Check we get the same data back out;
        self.assertEqual(data, sm.persistable_data)


class TestAddRecipe(TestCase):
    """Tests the add_recipe method."""

    @pfx.use_test_database
    def test_can_add_recipe(self) -> None:
        """Checks we can add a recipe to the meal."""
        # Create an empty meal instance;
        sm = model.meals.SettableMeal()

        # Assert there are no recipes;
        self.assertEqual(0, len(sm.recipes))

        # Add a recipe;
        sm.add_recipe(recipe_unique_name="Porridge", recipe_qty_data=qfx.get_qty_data(qty_in_g=300))

        # Assert the recipe is now on the instance;
        self.assertEqual(1, len(sm.recipes))
        self.assertTrue(sm.recipes[0].name == "Porridge")

        # Add another recipe;
        sm.add_recipe(recipe_unique_name="Banana Milkshake", recipe_qty_data=qfx.get_qty_data(qty_in_g=250))

        # Assert the recipe is now on the instance;
        self.assertEqual(2, len(sm.recipes))
        self.assertTrue(sm.recipes[1].name == "Banana Milkshake")


class TestTotalMealMass(TestCase):
    """Checks the total_meal_mass property."""

    @pfx.use_test_database
    def test_correct_value_is_returned(self):
        """Check we get the correct total meal mass back."""
        # Create a test instance, passing this data in;
        sm = model.meals.SettableMeal(meal_data={
            model.recipes.get_datafile_name_for_unique_value("Porridge"): qfx.get_qty_data(500),
            model.recipes.get_datafile_name_for_unique_value("Banana Milkshake"): qfx.get_qty_data(300),
            model.recipes.get_datafile_name_for_unique_value("Avocado and Prawns"): qfx.get_qty_data(200)
        })

        # Check the quantity is correct;
        self.assertEqual(1000, sm.total_meal_mass_g)

# class TestRecipeRatios(TestCase):
#     """Tests for the recipes property."""
#
#     @pfx.use_test_database
#     def test_returns_correct_recipe_ratios(self):
#         """Checks that the property returns the correct recipe ratios."""
#
#         # Create a test instance;
#         mb = model.meals.SettableMeal(meal_data={
#             rfx.DF_NAMES["Porridge"]: qfx.get_qty_data(500),
#             rfx.DF_NAMES["Banana Milkshake"]: qfx.get_qty_data(300),
#             rfx.DF_NAMES["Avocado and Prawns"]: qfx.get_qty_data(200)
#         })
#
#         # Check we get the correct recipe ratio instances back;
#         recipe_ratios = mb.recipe_ratios
#
#         # Check we get the correct number of recipe ratios back;
#         self.assertEqual(3, len(recipe_ratios))
#
#         # Check we get the correct recipe names back;
#         self.assertTrue(rfx.DF_NAMES["Porridge"] in recipe_ratios.keys())
#         self.assertTrue(rfx.DF_NAMES["Banana Milkshake"] in recipe_ratios.keys())
#         self.assertTrue(rfx.DF_NAMES["Avocado and Prawns"] in recipe_ratios.keys())
#
#         # Check the recipes have the correct ratios;
#         self.assertEqual(0.5, recipe_ratios[rfx.DF_NAMES["Porridge"]].subject_g_per_host_g)
#         self.assertEqual(0.3, recipe_ratios[rfx.DF_NAMES["Banana Milkshake"]].subject_g_per_host_g)
#         self.assertEqual(0.2, recipe_ratios[rfx.DF_NAMES["Avocado and Prawns"]].subject_g_per_host_g)
#
#         # Check they are the correct type;
#         for rr in recipe_ratios.values():
#             self.assertTrue(isinstance(rr, model.recipes.SettableRecipeRatio))
