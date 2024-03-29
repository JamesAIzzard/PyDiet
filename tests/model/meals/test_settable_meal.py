"""Tests for the MealBase class."""
from unittest import TestCase

import model.meals
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


class TestUniqueRecipeNames(TestCase):
    """Tests the recipe_names property."""

    @pfx.use_test_database
    def test_empty_list_returned_when_no_recipes_assigned(self):
        """Checks we get an empty list when there are no recipes assigned."""
        # Create an empty test instance;
        sm = model.meals.SettableMeal()

        # Assert there are no names in the list;
        self.assertEqual([], sm.unique_recipe_names)

    @pfx.use_test_database
    def test_correct_names_returned_when_recipes_assigned(self):
        """Checks that we get the correct names back if there are recipes assigned."""
        # Create a test instance, passing some recipes in;
        sm = model.meals.SettableMeal(meal_data={
            model.recipes.get_datafile_name_for_unique_value("Porridge"): qfx.get_qty_data(500),
            model.recipes.get_datafile_name_for_unique_value("Banana Milkshake"): qfx.get_qty_data(300),
            model.recipes.get_datafile_name_for_unique_value("Avocado and Prawns"): qfx.get_qty_data(200)
        })

        # Assert the correct names are in the recipes list;
        self.assertEqual({"Porridge", "Banana Milkshake", "Avocado and Prawns"}, set(sm.unique_recipe_names))


class TestAddRecipe(TestCase):
    """Tests the add_recipe method."""

    @pfx.use_test_database
    def test_can_add_recipe_with_qty_data(self) -> None:
        """Checks we can add a recipe to the meal."""
        # Create an empty meal instance;
        sm = model.meals.SettableMeal()

        # Assert there are no recipes;
        self.assertEqual(0, len(sm.recipes))

        # Add a recipe;
        sm.add_recipe(recipe_unique_name="Porridge", recipe_qty_data=qfx.get_qty_data(qty_in_g=300))

        # Assert the recipe is now on the instance;
        self.assertEqual(1, len(sm.recipes))
        self.assertTrue(sm.recipes[model.recipes.get_datafile_name_for_unique_value("Porridge")].name == "Porridge")

        # Add another recipe;
        sm.add_recipe(recipe_unique_name="Banana Milkshake", recipe_qty_data=qfx.get_qty_data(qty_in_g=250))

        # Assert the recipe is now on the instance;
        self.assertEqual(2, len(sm.recipes))
        self.assertTrue(
            sm.recipes[model.recipes.get_datafile_name_for_unique_value("Banana Milkshake")].name == "Banana Milkshake")

    @pfx.use_test_database
    def test_can_add_empty_recipe(self):
        """Checks we can add a recipe without specifying its quantity."""
        # Create test instance;
        sm = model.meals.SettableMeal()

        # Assert there are no recipes;
        self.assertEqual(0, len(sm.recipes))

        # Add a recipe without specifying quantity data;
        sm.add_recipe(recipe_unique_name="Porridge")

        # Check it was added;
        self.assertEqual(1, len(sm.recipes))
        self.assertTrue("Porridge" in sm.unique_recipe_names)

        # Check its quantity is undefined;
        self.assertFalse(sm.get_recipe_quantity(unique_name="Porridge").quantity_is_defined)


class TestTotalRecipesMass(TestCase):
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
        self.assertEqual(1000, sm.total_recipes_mass_g)


class TestRecipeQuantities(TestCase):
    """Tests for the recipe_quantities property."""

    @pfx.use_test_database
    def test_returns_correct_quantities(self):
        """Checks we get the correct quantities back."""
        # Grab datafile names for some recipes, we'll need them;
        p_dfn = model.recipes.get_datafile_name_for_unique_value("Porridge")
        bm_dfn = model.recipes.get_datafile_name_for_unique_value("Banana Milkshake")
        aap_dfn = model.recipes.get_datafile_name_for_unique_value("Avocado and Prawns")

        # Create a test instance;
        mb = model.meals.SettableMeal(meal_data={
            p_dfn: qfx.get_qty_data(500),
            bm_dfn: qfx.get_qty_data(300),
            aap_dfn: qfx.get_qty_data(200)
        })

        recipe_quantities = mb.recipe_quantities

        # Check we get the correct number of quantities back;
        self.assertEqual(3, len(recipe_quantities))

        # Check we get the correct recipe names back;
        self.assertTrue(p_dfn in recipe_quantities.keys())
        self.assertTrue(bm_dfn in recipe_quantities.keys())
        self.assertTrue(aap_dfn in recipe_quantities.keys())

        # Check the recipes have the correct ratios;
        self.assertEqual(500, recipe_quantities[p_dfn].quantity_in_g)
        self.assertEqual(300, recipe_quantities[bm_dfn].quantity_in_g)
        self.assertEqual(200, recipe_quantities[aap_dfn].quantity_in_g)

        # Check they are the correct type;
        for rr in recipe_quantities.values():
            self.assertTrue(isinstance(rr, model.recipes.ReadonlyRecipeQuantity))


class TestRecipeRatios(TestCase):
    """Tests for the recipe ratios property."""

    @pfx.use_test_database
    def test_returns_correct_recipe_ratios(self):
        """Checks that the property returns the correct recipe ratios."""

        # Grab datafile names for some recipes, we'll need them;
        p_dfn = model.recipes.get_datafile_name_for_unique_value("Porridge")
        bm_dfn = model.recipes.get_datafile_name_for_unique_value("Banana Milkshake")
        aap_dfn = model.recipes.get_datafile_name_for_unique_value("Avocado and Prawns")

        # Create a test instance;
        mb = model.meals.SettableMeal(meal_data={
            p_dfn: qfx.get_qty_data(500),
            bm_dfn: qfx.get_qty_data(300),
            aap_dfn: qfx.get_qty_data(200)
        })

        # Check we get the correct recipe ratio instances back;
        recipe_ratios = mb.recipe_ratios

        # Check we get the correct number of recipe ratios back;
        self.assertEqual(3, len(recipe_ratios))

        # Check we get the correct recipe names back;
        self.assertTrue(p_dfn in recipe_ratios.keys())
        self.assertTrue(bm_dfn in recipe_ratios.keys())
        self.assertTrue(aap_dfn in recipe_ratios.keys())

        # Check the recipes have the correct ratios;
        self.assertEqual(0.5, recipe_ratios[p_dfn].subject_g_per_host_g)
        self.assertEqual(0.3, recipe_ratios[bm_dfn].subject_g_per_host_g)
        self.assertEqual(0.2, recipe_ratios[aap_dfn].subject_g_per_host_g)

        # Check they are the correct type;
        for rr in recipe_ratios.values():
            self.assertTrue(isinstance(rr, model.recipes.ReadonlyRecipeRatio))


class TestGetRecipeQuantity(TestCase):
    """Tests for the `get_recipe_quantity` method."""

    @pfx.use_test_database
    def test_gets_correct_recipe_quantity(self):
        """Checks we can get the recipe quantity correctly."""
        # Create a test instance, passing this data in;
        sm = model.meals.SettableMeal(meal_data={
            model.recipes.get_datafile_name_for_unique_value("Porridge"): qfx.get_qty_data(500),
            model.recipes.get_datafile_name_for_unique_value("Banana Milkshake"): qfx.get_qty_data(300),
            model.recipes.get_datafile_name_for_unique_value("Avocado and Prawns"): qfx.get_qty_data(200)
        })

        # Grab the recipe quantity;
        rq = sm.get_recipe_quantity(unique_name="Porridge")

        # Check we get a recipe quantity of the right type;
        self.assertTrue(isinstance(rq, model.recipes.ReadonlyRecipeQuantity))

        # Check it has the right name;
        self.assertEqual("Porridge", rq.recipe.name)

        # Check it has the correct quantity;
        self.assertEqual(500, rq.quantity_in_g)


class TestSetRecipeQuantity(TestCase):
    """Tests for the `set_recipe_quantity` method."""

    @pfx.use_test_database
    def test_can_set_recipe_quantity(self):
        """Checks we can set the recipe quantity."""
        # Create a test instance, passing this data in;
        sm = model.meals.SettableMeal(meal_data={
            model.recipes.get_datafile_name_for_unique_value("Porridge"): qfx.get_qty_data(500),
            model.recipes.get_datafile_name_for_unique_value("Banana Milkshake"): qfx.get_qty_data(300),
            model.recipes.get_datafile_name_for_unique_value("Avocado and Prawns"): qfx.get_qty_data(200)
        })

        # Check the state of one of the recipe quantities, to confirm it is what we set it to be
        # in the constructor;
        self.assertEqual(500, sm.get_recipe_quantity(unique_name="Porridge").quantity_in_g)

        # Go ahead and change it;
        sm.set_recipe_quantity(recipe_unique_name="Porridge", quantity=0.6, unit="kg")

        # Now check it was changed;
        self.assertEqual(
            600,
            sm.get_recipe_quantity(unique_name="Porridge").quantity_in_g
        )


class TestIngredientUniqueNames(TestCase):
    """Tests the ingredient_unique_names property."""
    @pfx.use_test_database
    def test_correct_names_are_returned(self):
        """Checks that we get the right names back."""
        # Create a test instance with some known ingredients;
        sm = model.meals.SettableMeal(meal_data={
            model.recipes.get_datafile_name_for_unique_value("Bread and Butter"): qfx.get_qty_data(500),
            model.recipes.get_datafile_name_for_unique_value("Peanut Butter Toast"): qfx.get_qty_data(300),
        })

        self.assertEqual(
            {"Bread (Wholemeal)", "Butter", "Peanut Butter"},
            set(sm.ingredient_unique_names)
        )


class TestDefinedNutrientRatioNames(TestCase):
    """Tests the defined nutrient ratios property."""

    @pfx.use_test_database
    def test_correct_nutrient_names(self):
        """Checks we get the correct nutrient names back."""
        # Create a test instance with some known ingredients;
        sm = model.meals.SettableMeal(meal_data={
            model.recipes.get_datafile_name_for_unique_value("Bread and Butter"): qfx.get_qty_data(500),
            model.recipes.get_datafile_name_for_unique_value("Peanut Butter Toast"): qfx.get_qty_data(300),
        })

        # Check the defined nutrients are what we expect;
        self.assertEqual({
            "alcohol",
            "carbohydrate",
            "fat",
            "saturated_fat",
            "monounsaturated_fat",
            "polyunsaturated_fat",
            "protein",
            "sodium"
        },
            set(sm.defined_nutrient_ratio_names)
        )


class TestNutrientRatios(TestCase):
    """Tests the nutrient ratios property."""

    @pfx.use_test_database
    def test_ratios_return_correct_value(self):
        """Checks the nutrient ratios are returned correctly."""
        # Create a test instance with some known ingredients;
        sm = model.meals.SettableMeal(meal_data={
            model.recipes.get_datafile_name_for_unique_value("Bread and Butter"): qfx.get_qty_data(500),
            model.recipes.get_datafile_name_for_unique_value("Peanut Butter Toast"): qfx.get_qty_data(300),
        })

        ratios = sm.nutrient_ratios_data
        answers = {
            'polyunsaturated_fat': {'subject_qty_data': {'quantity_in_g': 0.034894957983193274, 'pref_unit': 'g'},
                                    'host_qty_data': {'quantity_in_g': 1, 'pref_unit': 'g'}},
            'alcohol': {'subject_qty_data': {'quantity_in_g': 0.0, 'pref_unit': 'g'},
                        'host_qty_data': {'quantity_in_g': 1, 'pref_unit': 'g'}},
            'sodium': {'subject_qty_data': {'quantity_in_g': 0.0031868907563025214, 'pref_unit': 'g'},
                       'host_qty_data': {'quantity_in_g': 1, 'pref_unit': 'g'}},
            'protein': {'subject_qty_data': {'quantity_in_g': 0.08552100840336135, 'pref_unit': 'g'},
                        'host_qty_data': {'quantity_in_g': 1, 'pref_unit': 'g'}},
            'monounsaturated_fat': {'subject_qty_data': {'quantity_in_g': 0.04777310924369748, 'pref_unit': 'g'},
                                    'host_qty_data': {'quantity_in_g': 1, 'pref_unit': 'g'}},
            'saturated_fat': {'subject_qty_data': {'quantity_in_g': 0.06905462184873949, 'pref_unit': 'g'},
                              'host_qty_data': {'quantity_in_g': 1, 'pref_unit': 'g'}},
            'carbohydrate': {'subject_qty_data': {'quantity_in_g': 0.4383865546218487, 'pref_unit': 'g'},
                             'host_qty_data': {'quantity_in_g': 1, 'pref_unit': 'g'}},
            'fat': {'subject_qty_data': {'quantity_in_g': 0.16844537815126054, 'pref_unit': 'g'},
                    'host_qty_data': {'quantity_in_g': 1, 'pref_unit': 'g'}}}

        for nutrient_name in ratios:
            self.assertAlmostEqual(
                answers[nutrient_name]['subject_qty_data']['quantity_in_g'],
                ratios[nutrient_name]['subject_qty_data']['quantity_in_g'],
                places=8
            )
